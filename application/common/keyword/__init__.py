from application.constant import ModuleStatus
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword

LIB_KEYWORD_MAP = {}
LIB_NAME_MAP = {}
LIB_ALIAS_MAP = {}
USER_KEYWORD_MAP = {}


def init_lib_keyword():
    lid_keywords = LibKeyword.objects.filter(
        status=ModuleStatus.NORMAL
    )
    for keyword in lid_keywords.iterator():
        data = {
            'name': keyword.name,
            'ext_name': keyword.ext_name,
            'input_params': keyword.input_params,
            'output_params': keyword.output_params,
        }
        LIB_KEYWORD_MAP[keyword.id] = data
        LIB_NAME_MAP[keyword.name] = keyword.ext_name
        LIB_ALIAS_MAP[keyword.ext_name] = keyword.name


def init_user_keyword():
    user_keywords = UserKeyword.objects.filter(
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


def update_user_keyword(user_keyword_id):
    user_keyword = UserKeyword.objects.filter(
        id=user_keyword_id,
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
