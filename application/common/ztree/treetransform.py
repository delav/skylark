import uuid
from django.conf import settings
from application.project.models import Project
from application.suitedir.serializers import SuiteDirSerializers
from application.testsuite.serializers import TestSuiteSerializers
from application.testcase.serializers import TestCaseSerializers
from application.common.handler import get_model_extra_data
from application.common.ztree.constant import NODE_DESC


def format_build_data(project_id, root_id=0):
    tree_nodes = []
    run_data = []
    project = Project.objects.get(id=project_id)
    dir_queryset = project.dirs.filter(category=settings.CATEGORY_META.get('TestCase'))
    dir_node_map = {}
    for dir_item in dir_queryset.iterator():
        dir_data = SuiteDirSerializers(dir_item).data
        dir_data['extra_data'] = get_model_extra_data(
            dir_item.id,
            settings.MODULE_TYPE_META.get('SuiteDir')
        )
        dir_node = fill_build_node(dir_data, '', 'dir')
        dir_node_map[dir_item.id] = dir_node
    for dir_item in dir_queryset:
        dir_node = dir_node_map.get(dir_item.id)
        # simple node
        if not dir_item.parent_dir_id:
            parent_id = root_id
        else:
            parent_id = dir_node_map[dir_item.parent_dir_id]['id']
        simple_dir_node = filter_simple_node(dir_node, parent_id)
        tree_nodes.append(simple_dir_node)

        suites = dir_item.suites
        dir_node['children'] = get_suite_tree(dir_node['id'], suites, tree_nodes)
        if not dir_item.parent_dir_id:
            dir_node['pid'] = root_id
            run_data.append(dir_node)
            continue
        parent_node = dir_node_map[dir_item.parent_dir_id]
        if 'children' not in parent_node:
            parent_node['children'] = []
        dir_node['pid'] = parent_node['id']
        parent_node['children'].append(dir_node)
    return project.name, run_data, tree_nodes


def get_suite_tree(dir_node_id, suite_queryset, tree_nodes):
    suite_tree = []
    for suite_item in suite_queryset.iterator():
        suite_data = TestSuiteSerializers(suite_item).data
        suite_data['extra_data'] = get_model_extra_data(
            suite_item.id,
            settings.MODULE_TYPE_META.get('TestSuite')
        )
        suite_node = fill_build_node(suite_data, dir_node_id, 'suite')
        case_queryset = suite_item.cases
        suite_node['children'] = []
        # simple node
        simple_suite_node = filter_simple_node(suite_node, dir_node_id)
        tree_nodes.append(simple_suite_node)
        for case_item in case_queryset.iterator():
            case_data = TestCaseSerializers(case_item).data
            case_data['extra_data'] = {}
            case_node = fill_build_node(case_data, suite_node['id'], 'case')
            suite_node['children'].append(case_node)
            # simple node
            simple_case_node = filter_simple_node(case_node, suite_node['id'])
            tree_nodes.append(simple_case_node)
        suite_tree.append(suite_node)
    return suite_tree


def fill_build_node(meta_data, parent_id, desc_key):
    return {
        'mid': meta_data.get('id'),
        'id': str(uuid.uuid1()),
        'pid': parent_id,
        'name': meta_data.get('name'),
        'desc': NODE_DESC[desc_key],
        'type': meta_data.get('category'),
        'meta': meta_data
    }


def filter_simple_node(item_node, parent_id):
    return {
        'mid': item_node.get('mid'),
        'id': item_node.get('id'),
        'pid': parent_id,
        'name': item_node.get('name'),
    }
