import json
from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.infra.client.redisclient import RedisClient
from application.infra.engine.dcsengine import DcsEngine
from application.infra.utils.buildhandler import *
from application.builder.models import Builder
from application.buildplan.models import BuildPlan
from application.buildhistory.models import BuildHistory
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
        try:
            plan_id = serializer.data['plan_id']
            plan = BuildPlan.objects.get(id=plan_id)
            batch_data = json.loads(plan.build_data)
            build = BuildHistory.objects.create(
                total_case=plan.total_case,
                build_plan_id=plan.id,
            )
            build_id = generate_test_build_id(build.id)
            task_id_list = []
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                task_id = f'{build_id}-{batch_no}'
                app.send_task(
                    settings.RUNNER_TASK,
                    queue=settings.RUNNER_QUEUE,
                    routing_key=settings.RUNNER_ROUTING_KEY,
                    args=(build_id, str(batch_no), suites, sources)
                )
                task_id_list.append(task_id)
            build.task_id = ','.join(task_id_list)
            build.save()
        except (Exception,) as e:
            logger.error(f'build failed: {e}')
            return JsonResponse(code=10100, msg='build failed')
        return JsonResponse(data={'build_id': build_id, 'total_case': plan.total_case})


class DebugBuilderViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Builder.objects.all()
    serializer_class = DebugBuildSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create debug run: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # debug mode don't save build data
            env_id = serializer.data['env_id']
            project_id = serializer.data['project_id']
            project_name = serializer.data['project_name']
            run_data = serializer.data['run_data']
            common_struct, structure_list = JsonParser(project_id, project_name, env_id, run_data).parse()
            engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
            engine.init_common_data(common_struct)
            engine.visit(structure_list)
            batch_data = engine.get_batch_data()
            build_id = generate_debug_build_id()
            # debug mode save batch to redis
            conn = RedisClient(settings.ROBOT_REDIS_URL).connector
            task_redis_key = settings.TASK_RESULT_KEY_PREFIX + build_id
            conn.hset(task_redis_key, 'batch', len(batch_data))
            task_id_list = []
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                task_id = f'{build_id}-{batch_no}'
                app.send_task(
                    settings.RUNNER_TASK,
                    queue=settings.RUNNER_QUEUE,
                    routing_key=settings.RUNNER_ROUTING_KEY,
                    args=(build_id, str(batch_no), suites, sources)
                )
                task_id_list.append(task_id)
        except (Exception,) as e:
            logger.error(f'build failed: {e}')
            return JsonResponse(code=10100, msg='build failed')
        return JsonResponse(data={'build_id': build_id, 'total_case': engine.get_case_count()})

    def retrieve(self, request, *args, **kwargs):
        build_id = kwargs.get('pk')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        current_build_result = conn.hgetall(settings.CASE_RESULT_KEY_PREFIX+build_id)
        logger.info("build progress: {}".format(current_build_result))
        return JsonResponse(data=current_build_result or {})




