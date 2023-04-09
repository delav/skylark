from datetime import date
from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.infra.client.redisclient import RedisClient
from application.infra.engine.dcsengine import DcsEngine
from application.infra.utils.buildhandler import *
from application.builder.models import Builder
from application.builder.serializers import TestBuildSerializers, DebugBuildSerializers
from application.common.parser.jsonparser import JsonParser
from skylark.celeryapp import app

# Create your views here.


class TestBuilderViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                          mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Builder.objects.all()
    serializer_class = TestBuildSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create test run: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_id = serializer.data.get('plan_id')
        app.send_task(
            settings.PERIODIC_TASK,
            queue=settings.PERIODIC_QUEUE,
            routing_key=settings.PERIODIC_ROUTING_KEY,
            args=(plan_id,)
        )
        return JsonResponse(data={'status': 'success'})


class DebugBuilderViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Builder.objects.all()
    serializer_class = DebugBuildSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create debug run: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # debug mode don't save build data
            env_id = serializer.data.get('env_id')
            region_id = serializer.data.get('region_id')
            project_id = serializer.data.get('project_id')
            project_name = serializer.data.get('project_name')
            run_data = serializer.data.get('run_data')
            common_struct, structure_list = JsonParser(project_id, project_name, env_id, region_id).parse(run_data)
            engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
            engine.init_common_data(common_struct)
            engine.visit(structure_list)
            batch_data = engine.get_batch_data()
            build_id = generate_debug_build_id()
            # debug mode save batch to redis
            conn = RedisClient(settings.ROBOT_REDIS_URL).connector
            task_redis_key = settings.TASK_RESULT_KEY_PREFIX + build_id
            conn.hset(task_redis_key, 'batch', len(batch_data))
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                app.send_task(
                    settings.RUNNER_TASK,
                    queue=settings.RUNNER_QUEUE,
                    routing_key=settings.RUNNER_ROUTING_KEY,
                    args=(build_id, str(batch_no), suites, sources)
                )
        except (Exception,) as e:
            logger.error(f'build failed: {e}')
            return JsonResponse(code=10100, msg='build failed')
        child_dir = date.today().strftime('%Y/%m/%d')
        report_path = str(settings.REPORT_PATH) + f'/{child_dir}/' + build_id
        build_result = {
            'build_id': build_id,
            'total_case': engine.get_case_count(),
            'report_path': report_path
        }
        return JsonResponse(data=build_result)

    def retrieve(self, request, *args, **kwargs):
        build_id = kwargs.get('pk')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        current_build_result = conn.hgetall(settings.CASE_RESULT_KEY_PREFIX+build_id)
        logger.info("build progress: {}".format(current_build_result))
        return JsonResponse(data=current_build_result or {})




