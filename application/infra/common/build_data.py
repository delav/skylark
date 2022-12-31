
content = {}


def select_entity(case_id):
    return str(case_id)


def format_tree(node, path):
    if not node:
        return
    if node.get('desc') == 'S':
        suite_content = ''
        for case in node.get('children'):
            case_id = case.get('mid')
            entity = select_entity(case_id)
            suite_content += entity
        content[path] = suite_content
        return
    if 'children' not in node:
        return
    for sub_node in node['children']:
        node_path = path + '.' + sub_node['name']
        if sub_node.get('desc') == 'D':
            content[node_path] = sub_node['meta']
        format_tree(sub_node, node_path)


if __name__ == '__main__':
    tree = {'cron_job': False, 'debug': True, 'data': {'id': 'b7a530a4-b417-4c59-82f1-e7e78d6ef81a', 'pid': 0, 'name': 'SKYLARK', 'desc': 'P', 'type': None, 'open': False, 'nocheck': True, 'checked': False, 'isParent': True, 'meta': {}, 'mid': 2, 'children': [{'id': 'e398434f-3d9b-49cf-becd-d212372adf8e', 'pid': 0, 'name': 'CASES', 'desc': 'D', 'type': 0, 'meta': {'id': 1, 'name': 'CASES', 'category': 0, 'parent_dir_id': None, 'project_id': 2, 'extra_data': {'variable': [], 'fixture': []}}, 'mid': 1, 'children': [{'id': 'ec8b2c66-f7f4-4bf5-a780-3cf81b56410b', 'pid': 'e398434f-3d9b-49cf-becd-d212372adf8e', 'name': 'suite1', 'desc': 'S', 'type': 0, 'meta': {'id': 1, 'name': 'suite8', 'category': 0, 'suite_dir_id': 1, 'timeout': None, 'extra_data': {'variable': [], 'fixture': []}}, 'mid': 1, 'children': [{'id': '1c477a8b-cfda-4ef6-8e24-377200308cdd', 'pid': 'ec8b2c66-f7f4-4bf5-a780-3cf81b56410b', 'name': '获取医院信息', 'desc': 'C', 'type': 0, 'meta': {'id': 18, 'name': '获取医院信息', 'category': 0, 'desc': None, 'priority_id': None, 'tags': [], 'test_suite_id': 1, 'inputs': None, 'outputs': None, 'timeout': None, 'extra_data': {'entity': [{'id': 70, 'input_args': '', 'output_args': '${out}', 'keyword_id': 2, 'keyword_type': 1, 'uuid': '9d49f278-576a-4e49-8d64-5e9c92eddf09'}, {'id': 71, 'input_args': '', 'output_args': '', 'keyword_id': 4, 'keyword_type': 1, 'uuid': '4690211d-e55b-4254-be9d-f8c055d4de3e'}, {'id': 72, 'input_args': '', 'output_args': '${out}', 'keyword_id': 2, 'keyword_type': 1, 'uuid': 'f6494c23-5817-4f7f-a884-403040d7cefc'}, {'id': 73, 'input_args': '', 'output_args': '${out}', 'keyword_id': 5, 'keyword_type': 1, 'uuid': '98e6093a-494e-4989-9c4e-0c48de5b8bd6'}, {'id': 74, 'input_args': '', 'output_args': '${out}', 'keyword_id': 2, 'keyword_type': 1, 'uuid': '4184dced-1ff3-44da-8501-e33dfe28ca63'}, {'id': 75, 'input_args': '', 'output_args': '${out}', 'keyword_id': 6, 'keyword_type': 1, 'uuid': '9f11e852-6481-4e82-b3c6-36a34be6fdc7'}]}}, 'mid': 18, 'children': []}]}]}]}}
    format_tree(tree['data'], 'SKYLARK')
    print(content)