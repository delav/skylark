from json import loads
from copy import deepcopy
from loguru import logger
from django.conf import settings
from infra.engine.dcsengine import DcsEngine
from infra.utils.typetransform import id_str_to_set
from application.status import ModuleStatus
from application.manager import get_project_by_id
from application.buildplan.models import BuildPlan
from application.buildrecord.models import BuildRecord
from application.projectversion.models import ProjectVersion
from application.buildhistory.models import BuildHistory
from application.common.parser.jsonparser import JsonParser
from application.manager import get_env_list, get_region_list
from application.builder.handler import generate_test_task_id
from skylark.celeryapp import app


@app.task
def periodic_builder(plan_id):
    """period task will execute real build task to run case"""
    plan_query = BuildPlan.objects.filter(
        id=plan_id,
        status=ModuleStatus.NORMAL
    )
    if not plan_query.exists():
        logger.warning(f'periodic builder not found plan: {plan_id}')
        return
    plan = plan_query.first()
    project = get_project_by_id(plan.project_id)
    if not project:
        logger.warning(f'periodic builder not found project: {plan.project_id}')
        return
    project_name = project.get('name')
    version_query = ProjectVersion.objects.filter(
        project_id=plan.project_id,
        branch=plan.branch
    )
    if not version_query.exists():
        logger.warning(f'periodic builder not found version: {plan.branch}')
        return
    version = version_query.first()
    env_list = id_str_to_set(plan.envs, to_int=True)
    region_list = id_str_to_set(plan.regions, to_int=True)
    run_data = loads(version.run_data)
    common_sources = loads(version.sources)
    if plan.auto_latest:
        build_cases = None
    else:
        build_cases = id_str_to_set(plan.build_cases, to_int=True)
    record = BuildRecord.objects.create(
        desc=plan.title,
        create_by=plan.create_by,
        plan_id=plan.id,
        project_id=plan.project_id,
        branch=plan.branch,
        envs=plan.envs,
        regions=plan.regions,
        periodic=True,
    )
    _create_task(
        record.id, plan.project_id, project_name, env_list,
        region_list, run_data, common_sources, build_cases
    )


@app.task
def instant_builder(record_id, project_id, project_name,
                    env_ids, region_ids, run_data, common_sources, auto_latest, build_cases):
    env_list = id_str_to_set(env_ids, to_int=True)
    region_list = id_str_to_set(region_ids, to_int=True)
    run_data = loads(run_data)
    common_sources = loads(common_sources)
    if auto_latest:
        build_cases = None
    else:
        build_cases = id_str_to_set(build_cases, to_int=True)
    _create_task(
        record_id, project_id, project_name, env_list,
        region_list, run_data, common_sources, build_cases
    )


def _create_task(record_id, project_id, project_name,
                 env_id_list, region_id_list, run_data, common_sources, build_cases):
    env_map = {item.get('id'): item.get('name') for item in get_env_list()}
    region_map = {item.get('id'): item.get('name') for item in get_region_list()}
    for env_id in env_id_list:
        env_name = env_map.get(env_id)
        if not env_name:
            logger.warning(f'create task not found env: {env_id}')
            continue
        env_common = common_sources.get(str(env_id))
        if not region_id_list:
            region_id, region_name = None, ''
            env_region_common = env_common.get('base')
            _execute(
                record_id, project_id, project_name, env_id, env_name,
                region_id, region_name, run_data, env_region_common, build_cases
            )
            continue
        for region_id in region_id_list:
            region_name = region_map.get(region_id)
            if not region_name:
                logger.warning(f'create task not found region: {region_id}')
                continue
            env_region_common = env_common.get(str(region_id))
            _execute(
                record_id, project_id, project_name, env_id, env_name,
                region_id, region_name, run_data, env_region_common, build_cases
            )


def _execute(record_id, project_id, project_name, env_id, env_name,
             region_id, region_name, run_data, env_region_common, build_cases):
    copy_data = deepcopy(run_data)
    common_struct, structure_list = JsonParser(
        project_id=project_id,
        project_name=project_name,
        env_id=env_id,
        region_id=region_id,
        include_cases=build_cases
    ).parse(copy_data, env_region_common, True)
    engine = DcsEngine(
        distributed=settings.DISTRIBUTED_BUILD,
        limit=settings.WORKER_MAX_CASE_LIMIT
    )
    engine.init_common_data(common_struct)
    engine.visit(structure_list)
    batch_data = engine.get_batch_data()
    batch = len(batch_data)
    instance = BuildHistory.objects.create(
        total_case=engine.get_case_count(),
        record_id=record_id,
        env_id=env_id,
        region_id=region_id,
        batch=batch,
    )
    instance.save()
    task_id = generate_test_task_id(instance.id)
    celery_task_list = []
    for batch_no, data in batch_data.items():
        suites, sources, resources, files = data[0], data[1], data[2], data[3]
        celery_task = app.send_task(
            settings.RUNNER_TASK,
            queue=settings.RUNNER_QUEUE,
            routing_key=settings.RUNNER_ROUTING_KEY,
            priority=1,
            args=(project_name, env_name, region_name, task_id, str(batch_no), suites, sources, resources, files)
        )
        celery_task_list.append(celery_task.id)
    instance.celery_task = ','.join(celery_task_list)
    instance.save()
