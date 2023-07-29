from application.region.models import Region


def get_region_id_map():
    result_map = {}
    queryset = Region.objects.all()
    for item in queryset.iterator():
        result_map[item.id] = item.name
    return result_map
