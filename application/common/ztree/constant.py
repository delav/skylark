# front tree root id
ROOT_ID = 0

# tree node base fields
base_node = {
    'id': 1,
    'pid': ROOT_ID,
    'mid': 1,
    'label': '',
    'category': 0,
    'desc': None,
    'type': 0,
    'open': False,
    'nocheck': True,
    'checked': False,
    'isParent': True,
    'menu': [],
    'action': [],
    'meta': {}
}

# front tree node desc
NODE_DESC = {
    'case': 'C',
    'suite': 'S',
    'dir': 'D',
    'root': 'P'
}
# action type
NODE_ACTION_TYPE = {
    'create': 1,
    'update': 2,
    'delete': 3,
    'upload': 4,
    'download': 5,
    'copy': 6,
    'paste': 7,
}

NODE_MENU = {
    'copy': {'title': '复制', 'type': NODE_ACTION_TYPE.get('copy'), 'action': {}},
    'paste': {'title': '粘贴', 'type': NODE_ACTION_TYPE.get('paste'), 'action': {}},
    'rename': {'title': '重命名', 'type': NODE_ACTION_TYPE.get('update'), 'action': {}},
    'delete': {'title': '删除', 'type': NODE_ACTION_TYPE.get('delete'), 'action': {}},
}

MENU_ACTION_MAP = {
    'rename_dir':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '目录名称'},
    'rename_test_suite':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '测试套件名'},
    'rename_keyword_file':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '关键字文件名'},
    'rename_resource_file':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '变量文件名'},
    'rename_project_file':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '文件名'},
    'rename_test_case':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '用例名'},
    'rename_cust_keyword':
        {'type': NODE_ACTION_TYPE.get('update'), 'title': '重命名', 'label': '组件名'},
    'delete_dir':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '目录及该目录下所有内容'},
    'delete_test_suite':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '套件及该套件下所有用例'},
    'delete_keyword_file':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '关键字文件'},
    'delete_resource_file':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '变量文件'},
    'delete_project_file':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '项目文件'},
    'delete_test_case':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '用例'},
    'delete_cust_keyword':
        {'type': NODE_ACTION_TYPE.get('delete'), 'title': '警告', 'text': '组件'},
    'copy_node':
        {'type': NODE_ACTION_TYPE.get('copy'), 'title': '复制节点', 'text': '复制成功'},
    'paste_node':
        {'type': NODE_ACTION_TYPE.get('paste'), 'title': '粘贴节点', 'text': '粘贴成功'}
}

NODE_ACTION_MAP = {
    'create_dir':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('dir'),
         'title': '新建目录', 'label': '目录名称', 'icon': 'iconfont icon-a-folderadd-line'},
    'create_test_suite':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('suite'),
         'title': '新建测试套件', 'label': '测试套件名', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_keyword_file':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('suite'),
         'title': '新建关键字套件', 'label': '关键字套件名', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_resource_file':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('suite'),
         'title': '新建变量文件', 'label': '变量文件名', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_project_file':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('suite'),
         'title': '新建项目文件', 'label': '文件名称', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_test_case':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('case'),
         'title': '新建测试用例', 'label': '用例名称', 'icon': 'iconfont icon-a-addline-line'},
    'create_cust_keyword':
        {'type': NODE_ACTION_TYPE.get('create'), 'desc': NODE_DESC.get('case'),
         'title': '新建关键字组件', 'label': '组件名称', 'icon': 'iconfont icon-a-addline-line'},
    'upload_project_file':
        {'type': NODE_ACTION_TYPE.get('upload'), 'desc': NODE_DESC.get('suite'),
         'title': '上传文件', 'label': '文件名称', 'icon': 'iconfont icon-a-cloudupload-line'},
    'download_project_file':
        {'type': NODE_ACTION_TYPE.get('download'), 'desc': NODE_DESC.get('suite'),
         'title': '下载文件', 'label': '文件名称', 'icon': 'iconfont icon-download'}
}

