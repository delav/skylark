from uuid import uuid1
from copy import deepcopy
from application.constant import *
from application.common.ztree.constant import *


def fill_base_node(**kwargs):
    node = deepcopy(base_node)
    node['id'] = str(uuid1())
    node['mid'] = kwargs.get('id')
    node['name'] = kwargs.get('name')
    node['type'] = kwargs.get('category')
    node['meta'] = kwargs
    return node


def fill_simple_node(**kwargs):
    node = deepcopy(simple_node)
    node.update(**kwargs)
    return node


def handler_case_node(case_data):
    node = fill_base_node(**case_data)
    node['desc'] = NODE_DESC['case']
    node['isParent'] = False
    rename_menu = deepcopy(NODE_MENU.get('rename'))
    delete_menu = deepcopy(NODE_MENU.get('delete'))
    if node['type'] == ModuleCategory.TESTCASE:
        node['nocheck'] = False
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_test_case')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_test_case')
        node['menu'] = [NODE_MENU.get('copy'), rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.KEYWORD:
        node['nocheck'] = True
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_cust_keyword')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_cust_keyword')
        node['menu'] = [NODE_MENU.get('copy'), rename_menu, delete_menu]
    return node


def handler_suite_node(suite_data):
    node = fill_base_node(**suite_data)
    node['desc'] = NODE_DESC['suite']
    rename_menu = deepcopy(NODE_MENU.get('rename'))
    delete_menu = deepcopy(NODE_MENU.get('delete'))
    if node['type'] == ModuleCategory.TESTCASE:
        node['nocheck'] = False
        node['isParent'] = True
        node['action'] = [NODE_ACTION_MAP.get('create_test_case')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_test_suite')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_test_suite')
        node['menu'] = [NODE_MENU.get('copy'), NODE_MENU.get('paste'), rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.KEYWORD:
        node['nocheck'] = True
        node['isParent'] = True
        node['action'] = [NODE_ACTION_MAP.get('create_cust_keyword')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_keyword_file')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_keyword_file')
        node['menu'] = [rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.VARIABLE:
        node['nocheck'] = True
        node['isParent'] = False
        node['action'] = []
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_variable_file')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_variable_file')
        node['menu'] = [rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.FILE:
        node['nocheck'] = True
        node['isParent'] = False
        node['action'] = [NODE_ACTION_MAP.get('download_project_file')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_project_file')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_project_file')
        node['menu'] = [rename_menu, delete_menu]
    return node


def handler_dir_node(dir_data):
    node = fill_base_node(**dir_data)
    node['desc'] = NODE_DESC['dir']
    node['action'] = [NODE_ACTION_MAP.get('create_dir')]
    node['isParent'] = True
    # parent dir, only show create dir action
    if dir_data.get('parent_dir_id') is None:
        if node['type'] == ModuleCategory.TESTCASE:
            node['nocheck'] = False
        return node
    # children dir
    rename_menu = deepcopy(NODE_MENU.get('rename'))
    delete_menu = deepcopy(NODE_MENU.get('delete'))
    rename_menu['action'] = MENU_ACTION_MAP.get('rename_dir')
    delete_menu['action'] = MENU_ACTION_MAP.get('delete_dir')
    if node['type'] == ModuleCategory.TESTCASE:
        node['nocheck'] = False
        node['action'].append(NODE_ACTION_MAP.get('create_test_suite'))
        node['menu'] = [NODE_MENU.get('paste'), rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.KEYWORD:
        node['nocheck'] = True
        node['action'].append(NODE_ACTION_MAP.get('create_keyword_file'))
        node['menu'] = [rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.VARIABLE:
        node['nocheck'] = True
        node['action'].append(NODE_ACTION_MAP.get('create_variable_file'))
        node['menu'] = [rename_menu, delete_menu]
    elif node['type'] == ModuleCategory.FILE:
        node['nocheck'] = True
        node['action'].append(NODE_ACTION_MAP.get('upload_project_file'))
        node['menu'] = [rename_menu, delete_menu]
    return node



