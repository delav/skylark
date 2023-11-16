import secrets


def common_data():
    return {
        'name': '',
        'desc': ''
    }


def create_build_hook_data():
    return {
        'plan_list': ''
    }


def create_git_hook_data():
    return {}


def generate_secret():
    return secrets.token_hex(16)
