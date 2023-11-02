from infra.robot.assembler.configure import Config
from application.constant import SPECIAL_SEP, VARIABLE_NAME_KEY, VARIABLE_VALUE_KEY

config = Config()


class VariableAssembler(object):

    def __init__(self, variable_list: list):
        self.variable_list = variable_list

    def _combine_variable_str(self, key, value):
        """
        combine variable key and value to string
        :param key: name
        :param value: value
        :return: combine str
        """
        return config.large_sep.join([key, value]) + config.linefeed

    def get_variables(self):
        variable_str = ''
        for item in self.variable_list:
            var_name = item.get(VARIABLE_NAME_KEY)
            var_value = self._get_value_str(item.get(VARIABLE_VALUE_KEY))
            variable_str += self._combine_variable_str(var_name, var_value)
        return variable_str

    def _get_value_str(self, value):
        if SPECIAL_SEP in value:
            value_list = value.split(SPECIAL_SEP)
            value_text = config.small_sep.join(value_list)
        else:
            value_text = value
        return value_text
