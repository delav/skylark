import uuid
from django.conf import settings
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.suitedir.serializers import SuiteDirSerializers
from application.testsuite.serializers import TestSuiteSerializers
from application.testcase.serializers import TestCaseSerializers
from application.common.handler import get_model_extra_data
from application.infra.constant.constants import FRONT_NODE_DESC


class Project2Tree(object):
    root_id = 0

    def __init__(self, project_id):
        self.project_id = project_id

    def get_case_nodes(self):
        tree_nodes = []
        project = Project.objects.get(id=self.project_id)
        project_data = ProjectSerializers(project).data
        project_node = self.fill_node(project_data, self.root_id, 'root')
        tree_nodes.append(project_node)
        dir_queryset = project.dirs.filter(category=settings.CATEGORY_META.get('TestCase'))
        dir_node_map = {}
        for dir_item in dir_queryset.iterator():
            dir_data = SuiteDirSerializers(dir_item).data
            dir_data['extra_data'] = get_model_extra_data(
                dir_item.id,
                settings.MODULE_TYPE_META.get('SuiteDir')
            )
            dir_node = self.fill_node(dir_data, '', 'dir')
            dir_node_map[dir_item.id] = dir_node

        for dir_item in dir_queryset.iterator():
            dir_node = dir_node_map[dir_item.id]
            if not dir_item.parent_dir_id:
                parent_node = project_node
            else:
                parent_node = dir_node_map[dir_item.parent_dir_id]
            dir_node['pid'] = parent_node['id']
            tree_nodes.append(dir_node)
            suite_queryset = dir_item.suites
            for suite_item in suite_queryset.iterator():
                suite_data = TestSuiteSerializers(suite_item).data
                suite_data['extra_data'] = get_model_extra_data(
                    suite_item.id,
                    settings.MODULE_TYPE_META.get('TestSuite')
                )
                suite_node = self.fill_node(suite_data, dir_node['id'], 'suite')
                tree_nodes.append(suite_node)
                case_queryset = suite_item.cases
                for case_item in case_queryset.iterator():
                    case_data = TestCaseSerializers(case_item).data
                    case_data['extra_data'] = {}
                    case_node = self.fill_node(case_data, suite_node['id'], 'case')
                    tree_nodes.append(case_node)
        return project.name, tree_nodes

    def fill_node(self, meta_data, parent_id, desc_key):
        return {
            'mid': meta_data.get('id'),
            'id': str(uuid.uuid1()),
            'pid': parent_id,
            'name': meta_data.get('name'),
            'desc': FRONT_NODE_DESC[desc_key],
            'type': meta_data.get('category'),
            'meta': meta_data
        }
