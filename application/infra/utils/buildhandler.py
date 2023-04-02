import uuid


def generate_debug_build_id():
    return str(uuid.uuid1())


def generate_test_build_id(id_digit):
    return str(id_digit)


def is_test_mode(build_id):
    return build_id.isdigit()


def generate_task_name(plan_id):
    return f'plan-{plan_id}'
