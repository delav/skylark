from application.infra.parser.builder import BaseBuilder


class VariableBuilder(BaseBuilder):
    """
    project common scalar
    """

    _name = 'common-'
    _suffix = '.txt'

    def __init__(self, project_name, env):
        super(VariableBuilder, self).__init__()
        self.env = env
        self.project_name = project_name

    def _variable_path(self):
        """
        get the variable path for header
        :return: string
        """
        return self.special_sep.join(
            [self.project_name, 'common', self._name, self.env, self._suffix]
        ) + self.linefeed

    def get_variable_info(self):
        """
        splice to robot resource string
        :return: string
        """
        return self._splice_str('Resource', self._variable_path())

