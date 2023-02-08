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
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        parser = JsonParser(project_id, project_name, serializer.data['run_data'], env_id).parse()
        try:
            instance = Builder(
                total_case=parser.case,
                build_by=request.user,
                cron_job=serializer.data['cron_job'],
                debug=serializer.data['debug'],
                env_id=env_id,
                project_id=project_id,
                build_data=json.dumps({'suite': parser.suite, 'data': parser.data})
            )
            instance.save()
        except (Exception,) as e:
            logger.error(f'build task failed: {e}')
            return JsonResponse(code=10100, msg='build task failed')

        build_id = instance.id
        engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
        engine.visit(parser)
        batch = engine.get_batch()
        conn.hset(f'{settings.TASK_RESULT_KEY_PREFIX}{build_id}', 'batch', batch)
        task_id_list = []
        for batch_no in range(1, batch+1):
            suite, data = engine.get(batch_no)
            task = app.send_task(
                'task.tasks.robot_runner',
                queue='runner',
                args=(str(build_id), str(batch_no), suite, data)
            )
            task_id_list.append(task.id)
        instance.task_id = ','.join(task_id_list)
        instance.save()
        return JsonResponse(data={'build_id': build_id, 'status': instance.status, 'total_case': engine.get_cases()})

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

