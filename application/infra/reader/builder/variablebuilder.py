from application.infra.reader.builder.basebuilder import BaseBuilder
from application.variable.models import Variable


class VariableBuilder(BaseBuilder):
    """
    project common scalar
    """

    _name = 'common-'
    _suffix = '.txt'

    def __init__(self, project_name, module_id, module_type, env='test'):
        self.env = env
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type
        self.constant_path = self._constant_path()

    def _constant_path(self):
        """
        get the variable path for header
        :return: string
        """
        return self.special_sep.join(
            [self.project_name, 'common', self._name, self.env, self._suffix]
        ) + self.linefeed

    def get_path(self):
        return self.constant_path

    def setting_info(self):
        """
        splice to robot resource string
        :return: string
        """
        return self._splice_str('Resource', self.constant_path)

    def variable_text(self):
        variable_str = ''
        var_queryset = Variable.objects.filter(
            env=self.env,
            module_id=self.module_id,
            module_type=self.module_type,
        )
        if not var_queryset.exists():
            return ''
        for item in var_queryset:
            variable_str += item.name + self.small_sep + item.value + self.linefeed
        return variable_str



