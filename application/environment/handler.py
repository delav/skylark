from application.environment.models import Environment


def get_env_id_map():
    result_map = {}
    queryset = Environment.objects.all()
    for item in queryset.iterator():
        result_map[item.id] = item.name
    return result_map
