from copy import deepcopy
from django.conf import settings


def fill_node(data: dict):
    node = deepcopy(settings.NODE)
    node.update(data)
    if node['type'] != 0:
        node['nocheck'] = True
    if node['desc'] == settings.NODE_DESC.get('TEST_CASE'):
        node['isParent'] = False
    return node
