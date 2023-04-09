import json
from django.conf import settings
from application.infra.engine.dcsengine import DcsEngine
from application.infra.utils.buildhandler import generate_test_build_id
from application.infra.utils.transform import id_str_to_set
from application.buildplan.models import BuildPlan
from application.projectversion.models import ProjectVersion
from application.buildhistory.models import BuildHistory
from application.common.parser.jsonparser import JsonParser
from skylark.celeryapp import app


@app.task
def periodic_builder(plan_id):
    """period task will execute real build task to run case"""
    plan = BuildPlan.objects.select_related('project').get(id=plan_id)
    version = ProjectVersion.objects.get(
        project_id=plan.project_id,
        branch=plan.branch
    )
    str_env_id_list = [plan.envs]
    if ',' in plan.envs:
        str_env_id_list = plan.envs.split(',')
    str_region_id_list = [plan.regions]
    if ',' in plan.regions:
        str_region_id_list = plan.regions.split(',')
    project_id = plan.project_id
    project_name = plan.project.name
    run_data = version.content
    common_sources = version.sources
    build_cases = id_str_to_set(plan.build_cases)
    for str_env_id in str_env_id_list:
        env_id = int(str_env_id)
        common = json.loads(common_sources)
        env_common = common.get(env_id)
        common_struct, structure_list = JsonParser(
            project_id=project_id,
            project_name=project_name,
            env_id=env_id,
            region_id=region_id,
            include_cases=build_cases
        ).parse(run_data, env_common)
        engine = DcsEngine(
            distributed=settings.DISTRIBUTED_BUILD,
            limit=settings.WORKER_MAX_CASE_LIMIT
        )
        engine.init_common_data(common_struct)
        engine.visit(structure_list)
        batch_data = engine.get_batch_data()
        batch = len(batch_data)
        instance = BuildHistory(
            total_case=engine.get_case_count(),
            build_plan_id=plan_id,
            batch=batch,
        )
        instance.save()
        build_id = generate_test_build_id(instance.id)
        celery_task_id_list = []
        for batch_no, data in batch_data.items():
            suites, sources = data[0], data[1]
            task = app.send_task(
                settings.RUNNER_TASK,
                queue=settings.RUNNER_QUEUE,
                routing_key=settings.RUNNER_ROUTING_KEY,
                args=(build_id, str(batch_no), suites, sources)
            )
            celery_task_id_list.append(task.id)
        instance.task_id = ','.join(celery_task_id_list)
        instance.save()
