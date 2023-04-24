import json
from datetime import datetime
from skylark.celeryapp import app
from application.projectversion.models import ProjectVersion
from application.environment.models import Environment
from application.region.models import Region
from application.common.parser.baseparser import CommonParser
from application.common.ztree.treetransform import format_build_data


@app.task
def generate_version(project_id, version_kwargs):
    project_name, run_data, nodes = format_build_data(project_id)
    env_resource_dict = {}
    env_queryset = Environment.objects.all()
    region_queryset = Region.objects.all()
    for env in env_queryset:
        if not region_queryset.exists():
            parser = CommonParser(project_id, project_name, env.id, None)
            parser.init_sources()
            env_resource_dict[env.id] = {}
            base_resource = {'base': {
                'variable_files': parser.common_variable_files,
                'resources': parser.common_resources,
                'project_files': parser.common_project_files,
            }}
            env_resource_dict[env.id].update(base_resource)
            continue
        for region in region_queryset:
            env_resource_dict[env.id] = {}
            parser = CommonParser(project_id, project_name, env.id, region.id)
            parser.init_sources()
            region_resource = {region.id: {
                'variable_files': parser.common_variable_files,
                'resources': parser.common_resources,
                'project_files': parser.common_project_files,
            }}
            env_resource_dict[env.id].update(region_resource)
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


