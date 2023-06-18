import uuid


def generate_debug_task_id():
    return str(uuid.uuid1())


def generate_test_task_id(id_digit):
    return str(id_digit)


def convert_test_task_id(build_id):
    return int(build_id)


def is_test_mode(build_id):
    return build_id.isdigit()


def generate_task_name(plan_id):
    return f'PLAN-{plan_id}'


def convert_task_name(task_name):
    return int(task_name.split('-')[1])