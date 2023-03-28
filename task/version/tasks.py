import json
from skylark.celeryapp import app
from application.projectversion.models import ProjectVersion
from application.environment.models import Environment
from application.common.ztree.treenode import Project2Tree
from application.common.parser.baseparser import BaseParser


@app.task
def generate_version(project_id, version_kwargs):
    project_name, node_content = Project2Tree(
        project_id).get_case_nodes()
    env_resource_dict = {}
    env_queryset = Environment.objects.all()
    for env in env_queryset.iterator():
        base_parser = BaseParser(project_id, project_name, env.id)
        base_parser.init_sources()
        env_resource_dict[env.id] = {
            'variable_files': base_parser.get_common_variable_files(),
            'resources': base_parser.get_common_resources(),
            'project_files': base_parser.get_common_project_files(),
        }
    version_kwargs['content'] = json.dumps(node_content)
    version_kwargs['sources'] = json.dumps(env_resource_dict)
    version = ProjectVersion.objects.filter(
        project_id=version_kwargs['project_id'],
        branch=version_kwargs['branch']
    )
    if version.exists():
        version.update(**version_kwargs)
        return
    ProjectVersion.objects.create(**version_kwargs)


