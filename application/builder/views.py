from datetime import date
from loguru import logger
from pathlib import Path
from django.conf import settings
from django.http import FileResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from infra.client.redisclient import RedisClient
from infra.engine.dcsengine import DcsEngine
from infra.utils.typetransform import join_id_to_str
from application.common.access.projectaccess import has_project_permission
from application.manager import get_project_by_id
from application.constant import (
    REDIS_CASE_RESULT_KEY_PREFIX, REDIS_TASK_RESULT_KEY_PREFIX, REDIS_DEBUG_RESULT_KEY_PREFIX
)
from application.buildplan.models import BuildPlan
from application.projectversion.models import ProjectVersion
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers
from application.buildhistory.models import BuildHistory
from application.builder.serializers import DebugBuildSerializers
from application.builder.serializers import TestQuickBuildSerializers, TestInstantBuildSerializers
from application.builder.handler import generate_test_task_id, generate_debug_task_id
from application.common.parser.jsonparser import JsonParser
from skylark.celeryapp import app

# Create your views here.


class BuilderViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def instant(self, request, *args, **kwargs):
        logger.info(f'test instant build: {request.data}')
        serializer = TestInstantBuildSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_id = serializer.validated_data.get('plan_id')
        env_list = serializer.validated_data.get('env_list')
        region_list = serializer.validated_data.get('region_list')
        plan_query = BuildPlan.objects.filter(id=plan_id)
        if not plan_query.exists():
            return JsonResponse(code=10001, msg='plan not found')
        plan = plan_query.first()
        project_id = plan.project_id
        project = get_project_by_id(project_id)
        if not project:
            return JsonResponse(code=10001, msg='project not exist')
        project_name = project.get('name')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        version = ProjectVersion.objects.get(
            project_id=project_id,
            branch=plan.branch
        )
        plan = BuildPlan.objects.get(id=plan_id)
        if not env_list:
            env_ids_str = plan.envs
        else:
            env_ids_str = join_id_to_str(env_list)
        if not region_list:
            region_ids_str = plan.regions
        else:
            region_ids_str = join_id_to_str(region_list)
        record = BuildRecord.objects.create(
            desc=plan.title,
            create_by=request.user.email,
            plan_id=plan_id,
            project_id=project_id,
            branch=plan.branch,
            envs=env_ids_str,
            regions=region_ids_str,
        )
        app.send_task(
            settings.INSTANT_TASK,
            queue=settings.RUNNER_QUEUE,
            args=(
                record.id, project_id, project_name, env_ids_str, region_ids_str,
                version.run_data, version.sources, plan.auto_latest, plan.build_cases
            )
        )
        result = BuildRecordSerializers(record).data
        return JsonResponse(data=result)

    @action(methods=['post'], detail=False)
    def quick(self, request, *args, **kwargs):
        logger.info(f'test quick build: {request.data}')
        serializer = TestQuickBuildSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.get('project_id')
        project_name = serializer.validated_data.get('project_name')
        branch = serializer.validated_data.get('branch')
        env_list = serializer.validated_data.get('env_list')
        region_list = serializer.validated_data.get('region_list')
        case_list = serializer.validated_data.get('case_list')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        version = ProjectVersion.objects.get(
            project_id=project_id,
            branch=branch
        )
        build_cases = join_id_to_str(case_list)
        auto_latest = False
        buidl_desc = f'QuickBuild-@{project_name}'
        env_ids_str = join_id_to_str(env_list)
        region_ids_str = join_id_to_str(region_list)
        record = BuildRecord.objects.create(
            desc=buidl_desc,
            create_by=request.user.email,
            project_id=project_id,
            branch=branch,
            envs=env_ids_str,
            regions=region_ids_str,
        )
        app.send_task(
            settings.INSTANT_TASK,
            queue=settings.RUNNER_QUEUE,
            args=(
                record.id, project_id, project_name,
                env_ids_str, region_ids_str, version.run_data, version.sources, auto_latest, build_cases
            )
        )
        result = BuildRecordSerializers(record).data
        return JsonResponse(data=result)

    @action(methods=['post'], detail=False)
    def debug(self, request, *args, **kwargs):
        logger.info(f'create debug run: {request.data}')
        serializer = DebugBuildSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        # debug mode don't save any data to db,  and build data from params
        env_id = serializer.validated_data.get('env_id')
        env_name = serializer.validated_data.get('env_name')
        region_id = serializer.validated_data.get('region_id')
        region_name = serializer.validated_data.get('region_name')
        project_id = serializer.validated_data.get('project_id')
        project_name = serializer.validated_data.get('project_name')
        run_data = serializer.validated_data.get('run_data')
        common_struct, structure_list = JsonParser(
            project_id, project_name, env_id, region_id
        ).parse(run_data)
        engine = DcsEngine(distributed=False, limit=settings.WORKER_MAX_CASE_LIMIT)
        engine.init_common_data(common_struct)
        engine.visit(structure_list)
        batch_data = engine.get_batch_data()
        task_id = generate_debug_task_id()
        # debug mode save batch to redis
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        task_redis_key = REDIS_TASK_RESULT_KEY_PREFIX + task_id
        conn.hset(task_redis_key, 'batch', len(batch_data))
        # waiting django-redis add feature to support hash
        # cache.hset(task_redis_key, 'batch', len(batch_data))
        for batch_no, data in batch_data.items():
            suites, sources, resources, files = data[0], data[1], data[2], data[3]
            app.send_task(
                settings.RUNNER_TASK,
                queue=settings.RUNNER_QUEUE,
                priority=0,
                args=(project_name, env_name, region_name, task_id, str(batch_no), suites, sources, resources, files)
            )
        child_dir = date.today().strftime('%Y/%m/%d')
        report_path = settings.REPORT_PATH.as_posix() + f'/{project_name}/{child_dir}/' + task_id
        build_result = {
            'build_id': task_id,
            'total_case': engine.get_case_count(),
        }
        log_redis_key = REDIS_DEBUG_RESULT_KEY_PREFIX + task_id
        conn.hmset(log_redis_key, {'report_path': report_path})
        conn.expire(log_redis_key, 3600)
        return JsonResponse(data=build_result)

    @action(methods=['post'], detail=False)
    def progress(self, request, *args, **kwargs):
        mode = request.data.get('mode')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        if mode == 'debug':
            task_id = request.data.get('task_id')
            redis_key = REDIS_CASE_RESULT_KEY_PREFIX + task_id
            current_build_result = conn.hgetall(redis_key)
            # current_build_result = cache.hgetall(redis_key)
            logger.debug("build progress: {}".format(current_build_result))
            return JsonResponse(data=current_build_result or {})
        record_id_list = request.data.get('records', [])
        redis_keys = []
        for record_id in record_id_list:
            histories = BuildHistory.objects.filter(record_id=record_id)
            for item in histories:
                task_id = generate_test_task_id(item.id)
                redis_keys.append(REDIS_CASE_RESULT_KEY_PREFIX + task_id)
        cases_result = conn.mget(redis_keys)
        # cases_result = cache.get_many(redis_keys)
        return JsonResponse(data=cases_result or [])

    @action(methods=['get'], detail=False)
    def log(self, request, *args, **kwargs):
        build_id = request.query_params.get('id')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        log_redis_key = REDIS_DEBUG_RESULT_KEY_PREFIX + build_id
        log_info = conn.hgetall(log_redis_key)
        log_file_name = 'log.html'
        file = Path(log_info.get('report_path', ''), log_file_name)
        if not file.is_file():
            return JsonResponse(code=40302, msg='report not found')
        stream = open(file, 'rb')
        response = FileResponse(stream)
        response['Content-Type'] = "application/octet-stream"
        response['Content-Disposition'] = f'attachment;filename={log_file_name}'
        response['Access-Control-Expose-Headers'] = "Content-Disposition"
        return response
