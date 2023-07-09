import copy
import uuid
from application.constant import *
from application.project.models import Project
from application.testsuite.models import TestSuite
from application.testcase.models import TestCase
from application.common.handler import get_model_simple_extra_data
from application.common.ztree.constant import NODE_DESC


def generate_build_data(project_id, root_id=0):
    tree_nodes = []
    run_data = []
    project = Project.objects.get(id=project_id)
    dir_queryset = project.dirs.filter(
        category=ModuleCategory.TESTCASE,
        status=ModuleStatus.NORMAL
    ).values('id', 'name', 'category', 'project_id', 'parent_dir_id')
    dir_node_map = {}
    simple_node_uid_map = {}
    for dir_data in dir_queryset.iterator():
        dir_data['extra_data'] = get_model_simple_extra_data(
            dir_data['id'],
            ModuleType.DIR
        )
        dir_node = fill_build_node(dir_data, 'dir')
        dir_node_map[dir_data['id']] = dir_node
        simple_node_uid_map[dir_data['id']] = str(uuid.uuid1())
    for dir_data in dir_queryset.iterator():
        dir_node = dir_node_map.get(dir_data['id'])
        parent_dir_id = dir_data['parent_dir_id']
        # simple node
        if not parent_dir_id:
            parent_id = root_id
        else:
            parent_id = simple_node_uid_map.get(parent_dir_id)
        simple_dir_node = filter_simple_node(dir_node, parent_id, 'dir')
        tree_nodes.append(simple_dir_node)
        suites = TestSuite.objects.filter(
            suite_dir_id=dir_data['id'],
            category=ModuleCategory.TESTCASE,
            status=ModuleStatus.NORMAL
        ).values('id', 'name', 'category', 'suite_dir_id', 'timeout')
        if 'children' not in dir_node:
            dir_node['children'] = []
        dir_node['children'].append(get_suite_tree(simple_dir_node['id'], suites, tree_nodes))
        if not parent_dir_id:
            run_data.append(dir_node)
            continue
        parent_node = dir_node_map[parent_dir_id]
        if 'children' not in parent_node:
            parent_node['children'] = []
        parent_node['children'].append(dir_node)
    return project.name, run_data, tree_nodes


def get_suite_tree(simple_dir_node_id, suite_queryset, tree_nodes):
    suite_tree = []
    for suite_data in suite_queryset.iterator():
        suite_data['extra_data'] = get_model_simple_extra_data(
            suite_data['id'],
            ModuleType.SUITE
        )
        suite_node = fill_build_node(suite_data, 'suite')
        case_queryset = TestCase.objects.filter(
            test_suite_id=suite_data['id'],
            category=ModuleCategory.TESTCASE,
            status=ModuleStatus.NORMAL
        ).values('id', 'name', 'category', 'test_suite_id', 'inputs', 'outputs', 'timeout')
        suite_node['children'] = []
        # simple node
        simple_suite_node = filter_simple_node(suite_node, simple_dir_node_id, 'suite')
        tree_nodes.append(simple_suite_node)
        for case_data in case_queryset.iterator():
            case_data['extra_data'] = get_model_simple_extra_data(
                case_data['id'],
                ModuleType.CASE,
                include_entity=True
            )
            case_node = fill_build_node(case_data, 'case')
            # simple node
            simple_case_node = filter_simple_node(case_node, simple_suite_node['id'], 'case')
            tree_nodes.append(simple_case_node)
            suite_node['children'].append(case_node)
        suite_tree.append(suite_node)
    return suite_tree


def fill_build_node(meta_data, desc_key):
    return {
        'mid': meta_data.get('id'),
        'name': meta_data.get('name'),
        'desc': NODE_DESC[desc_key],
        'type': meta_data.get('category'),
        'meta': copy.deepcopy(meta_data)
    }


def filter_simple_node(item_node, parent_id, desc_key):
    return {
        'mid': item_node.get('mid'),
        'id': item_node.get('id'),
        'pid': parent_id,
        'name': item_node.get('name'),
        'desc': NODE_DESC[desc_key],
    }
