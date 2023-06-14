from application.constant import KEYWORD_TYPE, KEYWORD_INPUT_TYPE

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
    user_type = KEYWORD_TYPE.get('UserKeyword')
    if keyword_data['keyword_type'] == user_type:
        keyword_data['input_type'] = handler_user_keyword_type(keyword_data['input_params'])
    return keyword_data


def handler_user_keyword_type(inputs):
    input_types = KEYWORD_INPUT_TYPE
    if inputs is None or inputs == '':
        return input_types.get('None')
    if '|' in inputs:
        return input_types.get('Multi')
    return input_types.get('Single')
