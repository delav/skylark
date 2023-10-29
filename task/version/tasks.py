import json
from datetime import datetime
from skylark.celeryapp import app
from infra.constant.constants import BASE_RESOURCE_KEY, USER_KEYWORD_KEY, VARIABLE_FILE_KEY, PROJECT_FILE_KEY
from application.constant import ModuleStatus
from application.projectversion.models import ProjectVersion
from application.environment.models import Environment
from application.region.models import Region
from application.common.parser.baseparser import CommonParser
from application.common.parser.treeformat import generate_version_data


@app.task
def generate_version(project_id, version_kwargs):
    project_name, run_data, nodes, case_number = generate_version_data(project_id)
    env_resource_dict = {}
    env_queryset = Environment.objects.all()
    region_queryset = Region.objects.filter(status=ModuleStatus.NORMAL)
    for env in env_queryset:
        env_resource_dict[env.id] = {}
        if not region_queryset.exists():
            parser = CommonParser(project_id, project_name, env.id, None)
            parser.init_sources()
            base_resource = {'base': {
                BASE_RESOURCE_KEY: parser.common_base_resources,
                USER_KEYWORD_KEY: parser.common_user_keywords,
                VARIABLE_FILE_KEY: parser.common_variable_files,
                PROJECT_FILE_KEY: parser.common_project_files,
            }}
            env_resource_dict[env.id].update(base_resource)
            continue
        for region in region_queryset:
            parser = CommonParser(project_id, project_name, env.id, region.id)
            parser.init_sources()
            region_resource = {region.id: {
                BASE_RESOURCE_KEY: parser.common_base_resources,
                USER_KEYWORD_KEY: parser.common_user_keywords,
                VARIABLE_FILE_KEY: parser.common_variable_files,
                PROJECT_FILE_KEY: parser.common_project_files,
            }}
            env_resource_dict[env.id].update(region_resource)
    version_kwargs['total_case'] = case_number
    version_kwargs['run_data'] = json.dumps(run_data)
    version_kwargs['nodes'] = json.dumps(nodes)
    version_kwargs['sources'] = json.dumps(env_resource_dict)
    version = ProjectVersion.objects.filter(
        project_id=version_kwargs['project_id'],
        branch=version_kwargs['branch']
    )
    if version.exists():
        version_kwargs['update_at'] = datetime.now()
        version.update(**version_kwargs)
        return
    ProjectVersion.objects.create(**version_kwargs)
    # TODO
    # send task to every slaver to pre-download file


