from application.infra.reader.builder.basebuilder import BaseBuilder
from application.constant.models import Variable
from application.suitedir.models import SuiteDir


class PublicResourceBuilder(BaseBuilder):
    """
    public resource include the public variables, and user customize keywords (no keywords in python file)
    """

    _name = 'common.txt'

    def __init__(self, project_id, project_name, env):
        super(PublicResourceBuilder, self).__init__()
        self.project_id = project_id
        self.project_name = project_name
        self.env = env
        self.variable_path = self.special_sep.join([project_name, 'common', self._name])

    def _splice_resource_path(self):
        """
        splice to robot resource string
        :return: string
        """
        return self._splice_str('Resource', self.variable_path)

    def _splice_key_value(self, key, value):
        return key + self.small_sep + value + self.linefeed

    def _get_public_variables(self):
        """
        get common resource setting
        :return: resource list
        """
        variable_content = ''
        queryset = Variable.objects.filter(
            module_id=self.project_id,
            module_type=0,
            env=self.env
        )
        if not queryset.exists():
            return {}
        for obj in queryset.iterator():
            variable_content += self._splice_key_value(obj.name, obj.value)
        return {self.variable_path: variable_content}

    def _get_customize_resource(self):
        """
        get customize resource
        :return: resource list
        """
        customize_resource_map = {}
        queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            dir_type=1
        )
        if queryset.exists():
            return {}
        dir_obj = queryset.first()
        dir_name = dir_obj.dir_name
        suites = dir_obj.suites.all()
        for suite_item in suites.iterator():
            resource_name = suite_item.suite_name
            resource_path = self.special_sep.join(self.project_name, dir_name, resource_name)
            resource_content = self._get_resource_content(suite_item.id)
            customize_resource_map.update({resource_path: resource_content})
        return customize_resource_map

    def _get_resource_content(self, suite_id):

        return ''

    def get_resource_quote(self, pro_obj, dir_obj):
        project_name = pro_obj.project_name
        return self._get_common_resource(project_name) + self._get_customize_resource(project_name, dir_obj)

    def get_resource_content(self):
        pass


class InitSuiteHeader(BaseBuilder):
    def __init__(self, module_id, module_type):
        super(InitSuiteHeader, self).__init__()
        self.module_id = module_id
        self.module_type = module_type

    def get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        obj = st_queryset.first()
        st_str = SetTearBuilder().get_from_object(obj)
        return st_str

    def get_variable(self):
        var_queryset = Variable.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        var_strs = VariableBuilder().get_from_queryset(var_queryset)
        return var_strs
