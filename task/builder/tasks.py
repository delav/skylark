import json
from django.conf import settings
from application.infra.engine.dcsengine import DcsEngine
from application.infra.utils.buildhandler import generate_test_task_id
from application.infra.utils.typetransform import id_str_to_set
from application.buildplan.models import BuildPlan
from application.buildrecord.models import BuildRecord
from application.projectversion.models import ProjectVersion
from application.buildhistory.models import BuildHistory
from application.common.parser.jsonparser import JsonParser
from skylark.celeryapp import app


@app.task
def periodic_builder(plan_id):
    """period task will execute real build task to run case"""
    plan = BuildPlan.objects.get(id=plan_id)
    version = ProjectVersion.objects.get(
        project_id=plan.project_id,
        branch=plan.branch
    )
    env_ids = id_str_to_set(plan.envs)
    region_ids = id_str_to_set(plan.regions)
    run_data = json.loads(version.run_data)
    common_sources = json.loads(version.sources)
    build_cases = id_str_to_set(plan.build_cases, to_int=True)
    record = BuildRecord.objects.create(
        create_by=plan.create_by,
        plan_id=plan.id,
        project_id=plan.project_id,
        branch=plan.branch,
        envs=plan.envs,
        regions=plan.regions,
        periodic=True,
    )
    _create_task(
        record.id, plan.project_id, plan.project_name, env_ids,
        region_ids, run_data, common_sources, build_cases
    )


@app.task
def instant_builder(record_id, project_id, project_name,
                    env_ids, region_ids, run_data, common_sources, build_cases):
    env_ids = id_str_to_set(env_ids)
    region_ids = id_str_to_set(region_ids)
    run_data = json.loads(run_data)
    common_sources = json.loads(common_sources)
    build_cases = id_str_to_set(build_cases, to_int=True)
    _create_task(
        record_id, project_id, project_name, env_ids,
        region_ids, run_data, common_sources, build_cases
    )


def _create_task(record_id, project_id, project_name,
                 env_id_list, region_id_list, run_data, common_sources, build_cases):
    for env_id in env_id_list:
        env_common = common_sources.get(env_id)
        if not region_id_list:
            region_id = None
            env_region_common = env_common.get('base')
            _execute(
                record_id, project_id, project_name, env_id,
                region_id, run_data, env_region_common, build_cases
            )
            continue
        for region_id in region_id_list:
            env_region_common = env_common.get(region_id)
            _execute(
                record_id, project_id, project_name, env_id,
                region_id, run_data, env_region_common, build_cases
            )


def _execute(record_id, project_id, project_name, env_id,
             region_id, run_data, env_region_common, build_cases):
    common_struct, structure_list = JsonParser(
        project_id=project_id,
        project_name=project_name,
        env_id=env_id,
        region_id=region_id,
        include_cases=build_cases
    ).parse(run_data, env_region_common)
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
        suites, sources = data[0], data[1]
        print(f"{batch_no}: {suites}")
        print(f"{batch_no}: {sources}")
        celery_task = app.send_task(
            settings.RUNNER_TASK,
            queue=settings.RUNNER_QUEUE,
            routing_key=settings.RUNNER_ROUTING_KEY,
            args=(task_id, str(batch_no), suites, sources)
        )
        celery_task_list.append(celery_task.id)
    instance.celery_task = ','.join(celery_task_list)
    instance.save()
