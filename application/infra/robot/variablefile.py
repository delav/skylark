from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.variables import Variables


class VariableFile(object):
    """
    common variables, separate file
    """

    def __init__(self, variable_list):
        self.variables = variable_list

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        return Variables(self.variables).get_variables()

    def get_text(self):
        return Config().variables_line + self._get_variables()
