from copy import deepcopy
from django.conf import settings


def fill_node(data: dict):
    node = deepcopy(settings.NODE)
    node.update(data)
    node_type = node['type']
    if node_type != 0:
        node['nocheck'] = True
    return node
