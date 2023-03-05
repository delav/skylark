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
from application.timertask.serializers import TimerTaskSerializers
from application.common.parser.jsonparser import JsonParser
from application.common.schedule.timer import DynamicTimer
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
        env_id = serializer.data['env_id']
        project_id = serializer.data['project_id']
        project_name = serializer.data['project_name']
        run_data = serializer.data['run_data']
        common_struct, structure_list = JsonParser(project_id, project_name, env_id, run_data).parse()
        engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
        engine.init_common_data(common_struct)
        engine.visit(structure_list)
        batch_data = engine.get_batch_data()
        batch = len(batch_data)
        try:
            instance = Builder(
                total_case=engine.get_case_count(),
                create_by=request.user,
                debug=serializer.data['debug'],
                env_id=env_id,
                project_id=project_id,
                batch=batch,
                build_data=json.dumps(batch_data)
            )
            instance.save()
        except (Exception,) as e:
            logger.error(f'build failed: {e}')
            return JsonResponse(code=10100, msg='build failed')
        build_id = instance.id
        task_id_list = []
        timer_info = serializer.data.get('timer_info' )
        if timer_info:
            timer_serializer = TimerTaskSerializers(data=timer_info)
            timer_serializer.is_valid(raise_exception=True)
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                task_args = (str(build_id), str(batch_no), suites, sources)
                task_name = f'{build_id}-{batch_no}'
                periodic_id = DynamicTimer(
                    timer_str=timer_serializer['timer_str'],
                    timer_type=timer_serializer['timer_type']
                ).save_task(task_name, settings.RUNNER_TASK, task_args, settings.RUNNER_QUEUE,
                            settings.RUNNER_ROUTING_KEY)
                task_id_list.append(periodic_id)
            timer_serializer.save()
            instance.timer_task_id = timer_serializer.data['id']
        else:
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                task_id = f'{build_id}-{batch_no}'
                app.send_task(
                    settings.RUNNER_TASK,
                    task_id=task_id,
                    queue=settings.RUNNER_QUEUE,
                    routing_key=settings.RUNNER_ROUTING_KEY,
                    args=(str(build_id), str(batch_no), suites, sources)
                )
                task_id_list.append(task_id)
            instance.task_id = ','.join(task_id_list)
        instance.save()
        return JsonResponse(data={'build_id': build_id, 'status': instance.status, 'total_case': instance.total_case})

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get build info: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10101, msg='build info not found')
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)


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
        app.send_task(settings.RUNNER_TASK,
                      queue=settings.RUNNER_QUEUE,
                      args=(build_id,)
                      )
        task_id_str = instance.task_id
        task_id_list = [task_id_str]
        if ',' in task_id_str:
            task_id_list = task_id_str.split(',')
        for task_id in task_id_list:
            app.control.revoke(task_id, terminate=True)
        instance.status = 9
        instance.save()
        return JsonResponse(data={'build_id': build_id, 'status': instance.status})

    def retrieve(self, request, *args, **kwargs):
        build_id = kwargs.get('pk')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        current_build_result = conn.hgetall(settings.CASE_RESULT_KEY_PREFIX+build_id)
        logger.info("build progress: {}".format(current_build_result))
        return JsonResponse(data=current_build_result or {})

