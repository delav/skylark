from django.conf import settings
from infra.client.gitclient import GitClient
from infra.utils.pythonscanner import scan_directory, get_functions_info
from application.status import KeywordCategory, KeywordParamMode
from application.usergroup.models import UserGroup
from application.libkeyword.models import LibKeyword


def scan_keyword(group_id_list, force_update=False):
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
    )
    all_func_list = []
    for group in user_group_queryset:
        absolute_path = settings.LIBRARY_FILE_DIR / group.library_path
        function_list = scan_directory(absolute_path)
        all_func_list.extend(function_list)
    return True, serializer_to_keyword(all_func_list)


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
    ready_func_list = []
    for func in func_list:
        func_name = func.get('name')
        keyword_query = LibKeyword.objects.filter(name=func_name)
        if keyword_query.exists() and not allowed_update:
            continue
        output_type = KeywordParamMode.NONE
        input_args = func.get('args')
        if len(input_args) == 0:
            input_type = KeywordParamMode.NONE
            if func.get('vararg'):
                input_type = KeywordParamMode.LIST
                input_args.append('*args')
            if func.get('kwarg'):
                input_type = KeywordParamMode.DICT
                input_args.append('**kwarg')
        else:
            input_type = KeywordParamMode.FINITE
            if func.get('vararg'):
                input_type = KeywordParamMode.MIXED
                input_args.append('*args')
            if func.get('kwarg'):
                input_type = KeywordParamMode.MIXED
                input_args.append('**kwarg')
        if func.get('returns'):
            returns = '${' + func.get('returns') + '}'
            output_type = KeywordParamMode.FINITE
        else:
            returns = None
        if input_args:
            input_args = '|'.join(input_args)
        ready_keyword_data = {
            'name': func_name,
            'ext_name': '',
            'desc': func.get('doc'),
            'group_id': None,
            'input_params': input_args,
            'input_desc': '',
            'output_params': returns,
            'output_desc': '',
            'input_type': input_type,
            'output_type': output_type,
            'category': KeywordCategory.CUSTOMIZED,
            'image': '',
            'status': -1,
            'source': func.get('module'),
            'mark': ''
        }
        ready_func_list.append(ready_keyword_data)
    return ready_func_list
