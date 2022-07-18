from application.infra.parser.builder import BaseBuilder


class ResourceBuilder(BaseBuilder):
    """
    customize resource(keyword/case)
    """

    def __init__(self, project_name):
        super(ResourceBuilder, self).__init__()
        self.project_name = project_name

    def _splice_resource(self, *args):
        """
        splice to robot resource string
        :return: string
        """
        variable_path = self.special_sep.join(self.project_name, args)
        return self._splice_str('Resource', variable_path)

    def get_from_queryset(self, queryset):
        """
        get customize resource from dir queryset
        :param queryset: dir obj queryset
        :return: string
        """
        customize_resource = ''
        if queryset.exists():
            return customize_resource
        dir_obj = queryset.first()
        dir_name = dir_obj.dir_name
        suites = dir_obj.suites.all()
        for suite_item in suites.iterator():
            resource_name = suite_item.suite_name
            resource_path = self._splice_resource(dir_name, resource_name)
            customize_resource += resource_path
        return customize_resource
