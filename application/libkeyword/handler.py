from django.conf import settings
from infra.client.gitclient import GitClient
from infra.utils.pythonscanner import scan_directory, get_functions_info
from infra.robot.utils.modulemathcher import check_python_module
from application.constant import KEYWORD_PARAMS_SEP
from application.status import KeywordCategory, KeywordParamMode, LibraryType
from application.usergroup.models import UserGroup
from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers
from application.pythonlib.models import PythonLib


def scan_library_and_keyword(group_id_list, force_update=False):
    git = GitClient()
    library_path = settings.LIBRARY_BASE_DIR / settings.LIBRARY_PROJECT_NAME
    # if not library_path.exists():
    #     need_update = True
    #     try:
    #         git.clone(settings.LIBRARY_GIT, settings.LIBRARY_BASE_DIR)
    #     except (Exception,):
    #         return False, 'git clone failed'
    # else:
    #     try:
    #         need_update = git.pull(library_path)
    #     except (Exception,):
    #         return False, 'git pull failed'
    # if not need_update and not force_update:
    #     return
    user_group_queryset = UserGroup.objects.filter(
        group_id__in=group_id_list
    ).select_related('group')
    all_func_list = get_group_func_list(user_group_queryset)
    result = {
        'ready_keywords': serializer_to_keyword(all_func_list),
        'operation_libraries': get_group_library_operation(user_group_queryset)
    }
    return True, result


def get_group_library_operation(user_groups):
    operation_libraries = {
        'delete': [],
        'update': [],
        'create': []
    }
    for group in user_groups:
        absolute_path = settings.LIBRARY_FILE_DIR / group.library_path
        group_modules = {}
        for f in absolute_path.iterdir():
            if check_python_module(f):
                module_name = f.name.split('.')[0]
                group_modules[module_name] = group.library_path
        group_library_queryset = PythonLib.objects.filter(
            user_group_id=group.group_id
        )
        exist_modules = {}
        for library in group_library_queryset:
            module = library.lib_name
            exist_modules[module] = library
            # delete not exist module
            if module not in group_modules:
                operation_libraries['delete'].append(library)
        for module, file_path in group_modules.items():
            if module in exist_modules:
                instance = exist_modules[module]
                # update exist module path
                if file_path != instance.lib_path:
                    instance.lib_path = file_path
                    operation_libraries['update'].append(instance)
            else:
                # create new module
                instance = PythonLib(
                    lib_name=module,
                    lib_type=LibraryType.CUSTOMIZED,
                    lib_path=file_path,
                    user_group_id=group.group_id
                )
                operation_libraries['create'].append(instance)
    return operation_libraries


def get_group_func_list(user_groups):
    group_func_list = []
    for group in user_groups:
        absolute_path = settings.LIBRARY_FILE_DIR / group.library_path
        function_list = scan_directory(absolute_path)
        group_func_list.extend(function_list)
    return group_func_list


def admin_scan_keyword(scan_files=None):
    git = GitClient()
    library_path = settings.LIBRARY_BASE_DIR / settings.LIBRARY_PROJECT_NAME
    if not library_path.exists():
        git.clone(settings.LIBRARY_GIT, settings.LIBRARY_BASE_DIR)
    else:
        git.pull(library_path)
    func_list = []
    if scan_files:
        for f in scan_files:
            full_path = settings.LIBRARY_FILE_DIR / f
            file_func_list = get_functions_info(full_path)
            func_list.extend(file_func_list)
    else:
        library_file_dir = settings.LIBRARY_FILE_DIR
        group_dir_list = [p for p in library_file_dir.glob('*') if p.is_dir()]
        for group_dir in group_dir_list:
            group_func_list = scan_directory(group_dir)
            func_list.extend(group_func_list)
    return serializer_to_keyword(func_list)


def serializer_to_keyword(func_list, allowed_update=False):
    serializer_func_list = []
    for func in func_list:
        func_name = func.get('name')
        keyword_query = LibKeyword.objects.filter(name=func_name)
        if keyword_query.exists() and not allowed_update:
            continue
        pr_info = get_params_return_info(func)
        if keyword_query.exists():
            keyword = keyword_query.first()
            old_pr_info = {
                'input_params': keyword.input_params,
                'output_params': keyword.output_params,
                'input_type': keyword.input_type,
                'output_type': keyword.output_type,
            }
            is_change = check_params_return_change(pr_info, old_pr_info)
            if is_change:
                update_keyword_data = LibKeywordSerializers(keyword).data
                update_keyword_data['new_info'] = pr_info
                serializer_func_list.append(update_keyword_data)
                continue
        ready_keyword_data = {
            'name': func_name,
            'ext_name': '',
            'desc': func.get('doc'),
            'group_id': None,
            'input_params': pr_info['input_params'],
            'input_desc': '',
            'output_params': pr_info['output_params'],
            'output_desc': '',
            'input_type': pr_info['input_type'],
            'output_type': pr_info['output_type'],
            'category': KeywordCategory.CUSTOMIZED,
            'image': '',
            'status': -1,
            'source': func.get('module'),
            'remark': ''
        }
        serializer_func_list.append(ready_keyword_data)
    return serializer_func_list


def get_params_return_info(func_data):
    input_args = func_data.get('args', [])
    if len(input_args) == 0:
        input_type = KeywordParamMode.NONE
        if func_data.get('vararg'):
            input_type = KeywordParamMode.LIST
            input_args.append('*args')
        if func_data.get('kwarg'):
            input_type = KeywordParamMode.DICT
            input_args.append('**kwarg')
    else:
        input_type = KeywordParamMode.FINITE
        if func_data.get('vararg'):
            input_type = KeywordParamMode.MIXED
            input_args.append('*args')
        if func_data.get('kwarg'):
            input_type = KeywordParamMode.MIXED
            input_args.append('**kwarg')
    if input_args:
        input_args = KEYWORD_PARAMS_SEP.join(input_args)
    if not func_data.get('returns'):
        returns = None
        output_type = KeywordParamMode.NONE
    else:
        returns = '${' + func_data.get('returns') + '}'
        output_type = KeywordParamMode.FINITE
    return {
        'input_params': input_args,
        'output_params': returns,
        'input_type': input_type,
        'output_type': output_type
    }


def check_params_return_change(new_info, old_info):
    param_change_flag, return_change_flag = False, False
    need_check_type = [
        KeywordParamMode.FINITE,
        KeywordParamMode.MIXED
    ]
    if new_info['input_type'] == old_info['input_type']:
        if new_info['input_type'] in need_check_type:
            if new_info['input_params'] != old_info['input_params']:
                param_change_flag = True
    elif new_info['input_type'] != old_info['input_type']:
        param_change_flag = True
    if new_info['output_type'] != old_info['output_type']:
        return_change_flag = True
    return param_change_flag or return_change_flag

