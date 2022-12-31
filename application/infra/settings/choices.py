# model data category. 0: test case, 1: resource(user keyword), 2: text/other file
CATEGORY_META = {
    'TestCase': 0,
    'Resource': 1,
    'HelpFile': 2,
}
CATEGORY = [(v, k) for k, v in CATEGORY_META.items()]

# related model data type
MODULE_TYPE_META = {
    'Project': 0,
    'SuiteDir': 1,
    'TestSuite': 2,
}
MODULE_TYPE = [(v, k) for k, v in MODULE_TYPE_META.items()]

# variable value type
VALUE_TYPE_META = {
    'String': 0,
    'Number': 1,
    'List': 2,
    'Dict': 3,
}
VALUE_TYPE = [(v, k) for k, v in VALUE_TYPE_META.items()]