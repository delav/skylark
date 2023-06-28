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
    'image': '',
    'status': 0
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
    return keyword_data


def handler_user_keyword_type(inputs):
    if inputs is None or inputs == '':
        return ParamMode.NAN
    elif '|' in inputs:
        return ParamMode.MULTI
    elif inputs == '@{LIST}':
        return ParamMode.LIST
    elif inputs == '&{DICT}':
        return ParamMode.DICT
    return ParamMode.SINGLE
