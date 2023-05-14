from datetime import date
from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from application.infra.django.response import JsonResponse
from application.infra.client.redisclient import RedisClient
from application.infra.engine.dcsengine import DcsEngine
from application.infra.utils.buildhandler import *
from application.infra.utils.typetransform import join_id_to_str
from application.projectversion.models import ProjectVersion
from application.buildplan.serializers import BuildPlanSerializers
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers
from application.builder.models import Builder
from application.builder.serializers import DebugBuildSerializers
from application.builder.serializers import TestQuickBuildSerializers
from application.common.parser.jsonparser import JsonParser
from skylark.celeryapp import app

# Create your views here.


class BuilderViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def instant(self, request, *args, **kwargs):
        logger.info(f'test instant build: {request.data}')
        serializer = BuildPlanSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_id = request.data.get('id')
        try:
            data = serializer.validated_data
            project_id = data.get('project_id')
            project_name = data.get('project_name')
            str_envs = data.get('envs')
            str_regions = data.get('regions')
            version = ProjectVersion.objects.get(
                project_id=project_id,
                branch=data.get('branch')
            )
            run_data = version.run_data
            common_sources = version.sources
            build_cases = data.get('build_cases')
            record = BuildRecord.objects.create(
                create_by=request.user.email,
                plan_id=plan_id,
                project_id=project_id,
                branch=data.get('branch'),
                envs=str_envs,
                regions=str_regions,
            )
        except (Exception,) as e:
            logger.error(f'instant build error: {e}')
            return JsonResponse(code=10200)
        app.send_task(
            settings.INSTANT_TASK,
            queue=settings.BUILDER_QUEUE,
            routing_key=settings.BUILDER_ROUTING_KEY,
            args=(
                record.id, project_id, project_name,
                str_envs, str_regions, run_data, common_sources, build_cases
            )
        )
        result = BuildRecordSerializers(record).data
        return JsonResponse(data=result)

    @action(methods=['post'], detail=False)
    def quick(self, request, *args, **kwargs):
        logger.info(f'test quick build: {request.data}')
        serializer = TestQuickBuildSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            project_id = serializer.validated_data.get('project_id')
            project_name = serializer.validated_data.get('project_name')
            branch = serializer.validated_data.get('branch')
            env_list = serializer.validated_data.get('env_list')
            region_list = serializer.validated_data.get('region_list')
            version = ProjectVersion.objects.get(
                project_id=project_id,
                branch=branch
            )
            run_data = version.run_data
            common_sources = version.sources
            build_cases = set(serializer.validated_data.get('case_list'))
            record = BuildRecord.objects.create(
                create_by=request.user.email,
                project_id=project_id,
                branch=branch,
                envs=join_id_to_str(env_list),
                regions=join_id_to_str(region_list),
            )
        except (Exception,) as e:
            logger.error(f'quick build error: {e}')
            return JsonResponse(code=10201)
        app.send_task(
            settings.INSTANT_TASK,
            queue=settings.BUILDER_QUEUE,
            routing_key=settings.BUILDER_ROUTING_KEY,
            args=(
                record.id, project_id, project_name,
                env_list, region_list, run_data, common_sources, build_cases
            )
        )
        result = BuildRecordSerializers(record).data
        return JsonResponse(data=result)

    @action(methods=['post'], detail=False)
    def debug(self, request, *args, **kwargs):
        logger.info(f'create debug run: {request.data}')
        serializer = DebugBuildSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # debug mode don't save build data
            env_id = serializer.validated_data.get('env_id')
            region_id = serializer.validated_data.get('region_id')
            project_id = serializer.validated_data.get('project_id')
            project_name = serializer.validated_data.get('project_name')
            run_data = serializer.validated_data.get('run_data')
            common_struct, structure_list = JsonParser(project_id, project_name, env_id, region_id).parse(run_data)
            engine = DcsEngine(distributed=settings.DISTRIBUTED_BUILD, limit=settings.WORKER_MAX_CASE_LIMIT)
            engine.init_common_data(common_struct)
            engine.visit(structure_list)
            batch_data = engine.get_batch_data()
            task_id = generate_debug_task_id()
            # debug mode save batch to redis
            conn = RedisClient(settings.ROBOT_REDIS_URL).connector
            task_redis_key = settings.TASK_RESULT_KEY_PREFIX + task_id
            conn.hset(task_redis_key, 'batch', len(batch_data))
            for batch_no, data in batch_data.items():
                suites, sources = data[0], data[1]
                app.send_task(
                    settings.RUNNER_TASK,
                    queue=settings.RUNNER_QUEUE,
                    routing_key=settings.RUNNER_ROUTING_KEY,
                    args=(task_id, str(batch_no), suites, sources)
                )
        except (Exception,) as e:
            logger.error(f'build failed: {e}')
            return JsonResponse(code=10100, msg='build failed')
        child_dir = date.today().strftime('%Y/%m/%d')
        report_path = str(settings.REPORT_PATH) + f'/{child_dir}/' + task_id
        build_result = {
            'build_id': task_id,
            'total_case': engine.get_case_count(),
            'report_path': report_path
        }
        return JsonResponse(data=build_result)

    @action(methods=['get'], detail=False)
    def progress(self, request, *args, **kwargs):
        build_id = kwargs.get('pk')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        current_build_result = conn.hgetall(settings.CASE_RESULT_KEY_PREFIX+build_id)
        logger.info("build progress: {}".format(current_build_result))
        return JsonResponse(data=current_build_result or {})




