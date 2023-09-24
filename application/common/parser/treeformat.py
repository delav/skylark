import uuid
from django.db.models import F
from application.constant import *
from application.project.models import Project
from application.suitedir.models import SuiteDir
from application.testsuite.models import TestSuite
from application.testcase.models import TestCase
from application.common.handler import get_model_simple_extra_data
from application.common.ztree.constant import NODE_DESC
from application.common.ztree.generatenode import fill_simple_node


def list_to_tree(node_list):
    result = []
    node_map = {}
    for node in node_list:
        cid = node['id']
        pid = node['parent_dir_id']
        if cid not in node_map:
            node_map[cid] = {'children': []}
        node_map[cid] = dict({'children': node_map.get(cid)['children']}, **node)
        tree_item = node_map[cid]
        if not pid:
            result.append(tree_item)
        else:
            if pid not in node_map:
                node_map[pid] = {'children': []}
            node_map[pid]['children'].append(tree_item)
    return result


def get_path_from_tree(tree_data, split='.'):
    result = {}
    if not tree_data:
        return result

    def parse_tree(data, parent_name=''):
        for item in data:
            node_name = item['name']
            if parent_name:
                node_name = split.join([parent_name, node_name])
            result[item['id']] = node_name
            if 'children' in item and item['children']:
                parse_tree(item['children'], node_name)
        return result
    return parse_tree(tree_data, '')


def parse_front_data(tree_data, split='.'):
    result = {'dirs': {}, 'suites': {}, 'cases': {}}
    if not tree_data:
        return result

    def parse_tree(data_list, parent_name=''):
        for item in data_list:
            if not item or not isinstance(item, dict):
                continue
            node_name = item['name']
            if parent_name:
                node_name = split.join([parent_name, node_name])
            _data = {'path': node_name, 'data': item['meta']}
            if item['desc'] == NODE_DESC['dir']:
                result['dirs'][item['mid']] = _data
                parse_tree(item['children'], node_name)
            if item['desc'] == NODE_DESC['suite']:
                result['suites'][item['mid']] = _data
                case_list = [mc['meta'] for mc in item['children']]
                result['cases'][item['mid']] = sorted(case_list, key=lambda x: (x['order'] is None, x['order']))
        return result
    return parse_tree(tree_data, '')


def generate_version_data(project_id, root_id=0):
    tree_nodes = []
    run_data = []
    project = Project.objects.get(id=project_id)
    dir_queryset = SuiteDir.objects.filter(
        project_id=project_id,
        category=ModuleCategory.TESTCASE,
        status=ModuleStatus.NORMAL
    ).values('id', 'name', 'category', 'project_id', 'parent_dir_id')
    dir_data_map = {}
    simple_node_uid_map = {}
    for item in dir_queryset.iterator():
        item['extra_data'] = get_model_simple_extra_data(
            item['id'],
            ModuleType.DIR
        )
        item['type'] = NODE_DESC.get('dir')
        dir_data_map[item['id']] = item
        simple_node_uid_map[item['id']] = str(uuid.uuid1())
    for item in dir_queryset.iterator():
        dir_data = dir_data_map.get(item['id'])
        parent_dir_id = item['parent_dir_id']
        # ztree node
        if not parent_dir_id:
            parent_id = root_id
        else:
            parent_id = simple_node_uid_map.get(parent_dir_id)
        node_id = simple_node_uid_map.get(item['id'])
        simple_dir_node = fill_simple_node(
            mid=dir_data['id'],
            id=node_id,
            pid=parent_id,
            name=dir_data['name'],
            desc=NODE_DESC['dir']
        )
        tree_nodes.append(simple_dir_node)

        suites = TestSuite.objects.filter(
            suite_dir_id=item['id'],
            category=ModuleCategory.TESTCASE,
            status=ModuleStatus.NORMAL
        ).values('id', 'name', 'category', 'suite_dir_id', 'timeout')
        if 'children' not in dir_data:
            dir_data['children'] = []
        if suites.exists():
            dir_data['children'].extend(_get_suite_tree(node_id, suites, tree_nodes))
        if not parent_dir_id:
            run_data.append(dir_data)
            continue
        parent_data = dir_data_map[parent_dir_id]
        if 'children' not in parent_data:
            parent_data['children'] = []
        parent_data['children'].append(dir_data)
    return project.name, run_data, tree_nodes


def _get_suite_tree(parent_node_id, suite_queryset, tree_nodes):
    suite_tree = []
    for suite_data in suite_queryset.iterator():
        suite_data['extra_data'] = get_model_simple_extra_data(
            suite_data['id'],
            ModuleType.SUITE
        )
        suite_data['type'] = NODE_DESC['suite']
        case_queryset = TestCase.objects.filter(
            test_suite_id=suite_data['id'],
            category=ModuleCategory.TESTCASE,
            status=ModuleStatus.NORMAL
        ).order_by(
            F('order').asc(nulls_last=True)
        ).values('id', 'name', 'category', 'test_suite_id', 'inputs', 'outputs', 'timeout')
        # ztree node
        suite_node_id = str(uuid.uuid1())
        simple_suite_node = fill_simple_node(
            mid=suite_data['id'],
            id=suite_node_id,
            pid=parent_node_id,
            name=suite_data['name'],
            desc=NODE_DESC['suite']
        )
        tree_nodes.append(simple_suite_node)
        if not case_queryset.exists():
            continue
        suite_data['children'] = []
        for case_data in case_queryset.iterator():
            case_data['extra_data'] = get_model_simple_extra_data(
                case_data['id'],
                ModuleType.CASE,
                include_entity=True
            )
            case_data['type'] = NODE_DESC['case']
            # ztree node
            simple_case_node = fill_simple_node(
                mid=case_data['id'],
                id=str(uuid.uuid1()),
                pid=suite_node_id,
                name=case_data['name'],
                desc=NODE_DESC['case']
            )
            tree_nodes.append(simple_case_node)

            suite_data['children'].append(case_data)
        suite_tree.append(suite_data)
    return suite_tree


def parse_version_data(tree_data, split='.'):
    result = {'dirs': {}, 'suites': {}, 'cases': {}}
    if not tree_data:
        return result

    def parse_tree(data, parent_name=''):
        for item in data:
            if not item or not isinstance(item, dict):
                continue
            item_name = item['name']
            if parent_name:
                item_name = split.join([parent_name, item_name])
            children = item.pop('children', [])
            _data = {'path': item_name, 'data': item}
            if item['type'] == NODE_DESC['dir']:
                result['dirs'][item['id']] = _data
                parse_tree(children, item_name)
            if item['type'] == NODE_DESC['suite']:
                result['suites'][item['id']] = _data
                result['cases'][item['id']] = children
        return result
    return parse_tree(tree_data, '')
