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
# extra entity key
FRONT_ENTITY_KEY = 'entity'

NODE_MENU = {
    'copy': {'title': '复制', 'type': 'copy', 'action': {}},
    'paste': {'title': '粘贴', 'type': 'paste', 'action': {}},
    'rename': {'title': '重命名', 'type': 'rename', 'action': {}},
    'delete': {'title': '删除', 'type': 'delete', 'action': {}},
}

MENU_ACTION_MAP = {
    'rename_dir':
        {'type': 'update', 'title': '重命名', 'label': '目录名称'},
    'rename_test_suite':
        {'type': 'update', 'title': '重命名', 'label': '测试套件名'},
    'rename_keyword_file':
        {'type': 'update', 'title': '重命名', 'label': '关键字文件名'},
    'rename_resource_file':
        {'type': 'update', 'title': '重命名', 'label': '变量文件名'},
    'rename_project_file':
        {'type': 'update', 'title': '重命名', 'label': '文件名'},
    'rename_test_case':
        {'type': 'update', 'title': '重命名', 'label': '用例名'},
    'rename_cust_keyword':
        {'type': 'update', 'title': '重命名', 'label': '组件名'},
    'delete_dir':
        {'type': 'delete', 'title': '警告', 'desc': '目录及该目录下所有内容'},
    'delete_test_suite':
        {'type': 'delete', 'title': '警告', 'desc': '套件及该套件下所有用例'},
    'delete_keyword_file':
        {'type': 'delete', 'title': '警告', 'desc': '关键字文件'},
    'delete_resource_file':
        {'type': 'delete', 'title': '警告', 'desc': '变量文件'},
    'delete_project_file':
        {'type': 'delete', 'title': '警告', 'desc': '项目文件'},
    'delete_test_case':
        {'type': 'delete', 'title': '警告', 'desc': '用例'},
    'delete_cust_keyword':
        {'type': 'delete', 'title': '警告', 'desc': '组件'},
}

NODE_ACTION_MAP = {
    'create_dir':
        {'type': 'create', 'title': '新建目录', 'label': '目录名称', 'icon': 'iconfont icon-a-folderadd-line'},
    'create_test_suite':
        {'type': 'create', 'title': '新建测试套件', 'label': '测试套件名', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_keyword_file':
        {'type': 'create', 'title': '新建关键字文件', 'label': '变量文件名', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_resource_file':
        {'type': 'create', 'title': '新建变量文件', 'label': '变量文件名', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_project_file':
        {'type': 'create', 'title': '新建项目文件', 'label': '文件名称', 'icon': 'iconfont icon-a-additionfile-line'},
    'create_test_case':
        {'type': 'create', 'title': '新建测试用例', 'label': '用例名', 'icon': 'iconfont icon-a-addline-line'},
    'create_cust_keyword':
        {'type': 'create', 'title': '新建关键字组件', 'label': '组件名', 'icon': 'iconfont icon-a-addline-line'},
    'upload_project_file':
        {'type': 'upload', 'title': '上传文件', 'label': '文件名称', 'icon': 'iconfont icon-edit'},
    'download_project_file':
        {'type': 'upload', 'title': '下载文件', 'label': '文件名称', 'icon': 'iconfont icon-edit'}
}

