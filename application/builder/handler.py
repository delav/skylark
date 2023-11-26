import uuid
from django.conf import settings
from skylark.celeryapp import app
from application.manager import get_project_by_id
from application.buildplan.models import BuildPlan
from application.projectversion.models import ProjectVersion
from application.buildrecord.models import BuildRecord
from application.common.access.projectaccess import has_project_permission


def generate_debug_task_id():
    return str(uuid.uuid1())


def generate_test_task_id(id_digit):
    return str(id_digit)


def convert_test_task_id(build_id):
    return int(build_id)


def is_test_mode(build_id):
    return build_id.isdigit()


def generate_task_name(plan_id):
    return f'PLAN-{plan_id}'


def convert_task_name(task_name):
    name_list = task_name.split('-')
    if len(name_list) != 2:
        return None
    if not name_list[1].isdigit():
        return None
    return int(name_list[1])


def execute_plan_by_id(plan_id, user):
    plan_query = BuildPlan.objects.filter(id=plan_id)
    if not plan_query.exists():
        return
    plan = plan_query.first()
    project_id = plan.project_id
    project = get_project_by_id(project_id)
    if not project:
        return
    project_name = project.get('name')
    version = ProjectVersion.objects.get(
        project_id=project_id,
        branch=plan.branch
    )
    plan = BuildPlan.objects.get(id=plan_id)
    if not has_project_permission(project_id, user):
        return
    env_ids_str = plan.envs
    region_ids_str = plan.regions
    record = BuildRecord.objects.create(
        desc=plan.title,
        create_by=user.email,
        plan_id=plan_id,
        project_id=project_id,
        branch=plan.branch,
        envs=env_ids_str,
        regions=region_ids_str,
    )
    app.send_task(
        settings.INSTANT_TASK,
        queue=settings.BUILDER_QUEUE,
        args=(
            record.id, project_id, project_name, env_ids_str, region_ids_str,
            plan.parameters, version.run_data, version.sources, plan.auto_latest, plan.build_cases
        )
    )
