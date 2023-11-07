from application.status import ModuleStatus

LIB_KEYWORD_MAP = {}
LIB_NAME_MAP = {}
LIB_ALIAS_MAP = {}
USER_KEYWORD_MAP = {}


def load_lib_keyword_to_storage(model):
    lib_keywords = model.objects.filter(
        status=ModuleStatus.NORMAL
    ).values('id', 'name', 'ext_name', 'input_params', 'output_params')
    for keyword in lib_keywords.iterator():
        item_data = {
            'name': keyword['name'],
            'ext_name': keyword['ext_name'],
            'input_params': keyword['input_params'],
            'output_params': keyword['output_params'],
        }
        LIB_KEYWORD_MAP[keyword['id']] = item_data
        LIB_NAME_MAP[keyword['name']] = keyword['ext_name']
        LIB_ALIAS_MAP[keyword['ext_name']] = keyword['name']


def load_user_keyword_to_storage(model):
    user_keywords = model.objects.filter(
        status=ModuleStatus.NORMAL
    ).select_related('test_case')
    for keyword in user_keywords.iterator():
        data = {
            'name': keyword.test_case.name,
            'ext_name': keyword.test_case.name,
            'input_params': keyword.test_case.inputs,
            'output_params': keyword.test_case.outputs
        }
        USER_KEYWORD_MAP[keyword.id] = data


def update_user_keyword_storage(model, case_id):
    user_keyword = model.objects.filter(
        test_case_id=case_id,
        status=ModuleStatus.NORMAL,
    ).select_related('test_case')
    if not user_keyword.exists():
        return
    user_keyword = user_keyword.first()
    data = {
        'name': user_keyword.test_case.name,
        'ext_name': user_keyword.test_case.name,
        'input_params': user_keyword.test_case.inputs,
        'output_params': user_keyword.test_case.outputs
    }
    USER_KEYWORD_MAP[user_keyword.id] = data
