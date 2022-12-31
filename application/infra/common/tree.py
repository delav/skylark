
def list_to_tree(node_list):
    result = []
    node_map = {}
    for node in node_list:
        cid = node['id']
        pid = node['parent_dir_id']
        if cid not in node_map:
            node_map[cid] = {'children': []}
        node_map[cid] = dict({'children': node_map.get(cid)['children']}, **node)
        tree_item = node_map[cid]
        if not pid:
            result.append(tree_item)
        else:
            if pid not in node_map:
                node_map[pid] = {'children': []}
            node_map[pid]['children'].append(tree_item)
    return result


def get_path_from_tree(tree_data, split='.'):
    result = {}
    if not tree_data:
        return result

    def parse_tree(data, parent_name=''):
        for item in data:
            node_name = item['name']
            if parent_name:
                node_name = split.join([parent_name, node_name])
            result[item['id']] = node_name
            if 'children' in item and item['children']:
                parse_tree(item['children'], node_name)
        return result
    return parse_tree(tree_data, '')
