import os
import json
from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.infra.client.redisclient import RedisClient
from application.infra.engine.dcsengine import DcsEngine
from application.builder.models import Builder
from application.builder.serializers import BuilderSerializers, BuildDataSerializers
from application.common.parser.jsonparser import JsonParser
from skylark.celeryapp import app

# Create your views here.


class BuilderViewSets(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get build list: {request.query_params}')
        return JsonResponse(data={})

    def create(self, request, *args, **kwargs):
        logger.info(f'create build: {request.data}')
        serializer = BuildDataSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        env_id = serializer.data['env']
        project_id = serializer.data['project_id']
        project_name = serializer.data['project_name']
        run_data = serializer.data['run_data']
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        common_struct, structure_list = JsonParser(project_id, project_name, run_data, env_id).parse()
        engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
        engine.init_common_data(common_struct)
        engine.visit(structure_list)
        batch_data = engine.get_batch_data()
        print(batch_data)
        try:
            instance = Builder(
                total_case=engine.get_case_count(),
                build_by=request.user,
                cron_job=serializer.data['cron_job'],
                debug=serializer.data['debug'],
                env_id=env_id,
                project_id=project_id,
                build_data=json.dumps(batch_data)
            )
            instance.save()
        except (Exception,) as e:
            logger.error(f'build task failed: {e}')
            return JsonResponse(code=10100, msg='build task failed')
        build_id = instance.id
        task_id_list = []
        if not instance.cron_job:
            batch = len(batch_data)
            redis_key = f'{settings.TASK_RESULT_KEY_PREFIX}{build_id}'
            conn.hset(redis_key, 'batch', batch)
            conn.expire(redis_key, settings.REDIS_EXPIRE_TIME)
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                task = app.send_task(
                    'task.tasks.robot_runner',
                    queue='runner',
                    args=(str(build_id), str(batch_no), suites, sources)
                )
                task_id_list.append(task.id)
            instance.task_id = ','.join(task_id_list)
            instance.save()
        else:
            # todo, build with cron job
            pass
        return JsonResponse(data={'build_id': build_id, 'status': instance.status, 'total_case': engine.total_case})

    def retrieve(self, request, *args, **kwargs):
        pass


class BuildEdgeViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Builder.objects.all()
    serializer_class = BuilderSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'stop build: {request.data}')
        serializer = BuildDataSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        build_id = request.data.get('build_id')
        try:
            instance = Builder.objects.get(id=build_id)
        except (Exception,) as e:
            logger.error(f'stop build failed: {e}')
            return JsonResponse(code=10200, msg='stop build failed')
        app.send_task('task.tasks.robot_runner',
                      queue='runner',
                      args=(build_id,)
                      )
        app.control.revoke(instance.task_id, terminate=True)
        instance.status = 9
        instance.save()
        return JsonResponse(data={'build_id': build_id, 'status': instance.status})

    def retrieve(self, request, *args, **kwargs):
        build_id = kwargs.get('pk')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        current_build_result = conn.hgetall(settings.CASE_RESULT_KEY_PREFIX+build_id)
        logger.info("build progress: {}".format(current_build_result))
        return JsonResponse(data=current_build_result or {})

