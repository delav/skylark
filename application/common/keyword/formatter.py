import re
from application.constant import KeywordType, ParamMode

fields = {
    'id': '',
    'name': '',
    'ext_name': '',
    'desc': '',
    'group_id': 1,
    'keyword_type': 1,
    'input_params': '',
    'output_params': '',
    'input_desc': '',
    'output_desc': '',
    'input_type': 2,
    'output_type': 0,
    'category': 0,
    'image': ''
}


def format_keyword_data(**kwargs):
    keyword_data = {}
    for key, value in fields.items():
        keyword_data[key] = kwargs.get(key, value)
    if not all([
        keyword_data['id'],
        keyword_data['name'],
        keyword_data['ext_name']
    ]):
        return {}
    if keyword_data['keyword_type'] == KeywordType.USER:
        keyword_data['input_type'] = handler_user_keyword_type(keyword_data['input_params'])
        keyword_data['output_type'] = ParamMode.NONE
    return keyword_data


def handler_user_keyword_type(inputs):
    if inputs is None or inputs == '':
        return ParamMode.NONE
    list_pattern = re.compile(r'\@\{(.*)\}')
    list_arg = list_pattern.search(inputs)
    if list_arg:
        return ParamMode.LIST
    dict_pattern = re.compile(r'\&|\&\{(.*)\}')
    dict_arg = dict_pattern.search(inputs)
    if dict_arg:
        return ParamMode.DICT
    elif '|' in inputs:
        return ParamMode.MULTI
    return ParamMode.SINGLE
