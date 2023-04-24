from uuid import uuid1
from copy import deepcopy
from django.conf import settings
from application.common.ztree.constant import *


def fill_base_node(base_data: dict):
    node = deepcopy(base_node)
    node['id'] = uuid1()
    node['mid'] = base_data.get('id')
    node['name'] = base_data.get('name')
    node['type'] = base_data.get('category')
    node['meta'] = base_data
    return node


def handler_case_node(case_data):
    node = fill_base_node(case_data)
    node['desc'] = NODE_DESC['case']
    node['isParent'] = False
    rename_menu = deepcopy(NODE_MENU.get('rename'))
    delete_menu = deepcopy(NODE_MENU.get('delete'))
    if node['type'] == settings.CATEGORY_META.get('TestCase'):
        node['nocheck'] = False
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_test_case')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_test_case')
        node['menu'] = [NODE_MENU.get('copy'), rename_menu, delete_menu]
    elif node['type'] == settings.CATEGORY_META.get('Keyword'):
        node['nocheck'] = True
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_cust_keyword')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_cust_keyword')
        node['menu'] = [NODE_MENU.get('copy'), rename_menu, delete_menu]
    return node


def handler_suite_node(suite_data):
    node = fill_base_node(suite_data)
    node['desc'] = NODE_DESC['suite']
    rename_menu = deepcopy(NODE_MENU.get('rename'))
    delete_menu = deepcopy(NODE_MENU.get('delete'))
    if node['type'] == settings.CATEGORY_META.get('TestCase'):
        node['nocheck'] = False
        node['isParent'] = True
        node['action'] = [NODE_ACTION_MAP.get('create_test_case')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_test_suite')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_test_suite')
        node['menu'] = [NODE_MENU.get('copy'), NODE_MENU.get('paste'), rename_menu, delete_menu]
    elif node['type'] == settings.CATEGORY_META.get('Keyword'):
        node['nocheck'] = True
        node['isParent'] = True
        node['action'] = [NODE_ACTION_MAP.get('create_cust_keyword')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_keyword_file')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_keyword_file')
        node['menu'] = [NODE_MENU.get('copy'), NODE_MENU.get('paste'), rename_menu, delete_menu]
    elif node['type'] == settings.CATEGORY_META.get('Resource'):
        node['nocheck'] = True
        node['isParent'] = False
        node['action'] = [NODE_ACTION_MAP.get('create_resource_file')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_resource_file')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_resource_file')
        node['menu'] = [NODE_MENU.get('copy'), NODE_MENU.get('paste'), rename_menu, delete_menu]
    elif node['type'] == settings.CATEGORY_META.get('ProjectFile'):
        node['nocheck'] = True
        node['isParent'] = False
        node['action'] = [NODE_ACTION_MAP.get('upload_project_file'), NODE_ACTION_MAP.get('download_project_file')]
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_project_file')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_project_file')
        node['menu'] = [rename_menu, delete_menu]
    return node


def handler_dir_node(dir_data):
    node = fill_base_node(dir_data)
    node['desc'] = NODE_DESC['dir']
    node['action'] = [NODE_ACTION_MAP.get('create_dir')]
    node['isParent'] = True
    # is child dir
    if dir_data.get('parent_dir_id') is not None:
        rename_menu = deepcopy(NODE_MENU.get('rename'))
        delete_menu = deepcopy(NODE_MENU.get('delete'))
        rename_menu['action'] = MENU_ACTION_MAP.get('rename_dir')
        delete_menu['action'] = MENU_ACTION_MAP.get('delete_dir')
        node['menu'].extend([rename_menu, delete_menu])
    if node['type'] == settings.CATEGORY_META.get('TestCase'):
        node['nocheck'] = False
        node['action'].append(NODE_ACTION_MAP.get('create_test_suite'))
    elif node['type'] == settings.CATEGORY_META.get('Keyword'):
        node['nocheck'] = True
        node['action'].append(NODE_ACTION_MAP.get('create_keyword_file'))
    elif node['type'] == settings.CATEGORY_META.get('Resource'):
        node['nocheck'] = True
        node['action'].append(NODE_ACTION_MAP.get('create_resource_file'))
    elif node['type'] == settings.CATEGORY_META.get('ProjectFile'):
        node['nocheck'] = True
        node['action'].append(NODE_ACTION_MAP.get('create_project_file'))
    return node



