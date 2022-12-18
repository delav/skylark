from application.infra.robot.assembler.config import Config

config = Config()


class VariableKey(object):

    def __init__(self, variable_name_key, variable_value_key):
        self.name_key = variable_name_key
        self.value_key = variable_value_key


class Variables(object):

    def __init__(self, variable_list: list, variable_key: VariableKey):
        self.variable_list = variable_list
        self.variable_key = variable_key

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
            var_name = item.get(self.variable_key.name_key)
            var_value = self._get_value_str(self.variable_key.value_key)
            variable_str += self._combine_variable_str(var_name, var_value)
        return variable_str

    def _get_value_str(self, value):
        if config.special_sep in value:
            value_list = value.split(config.special_sep.special_sep)
            value_text = config.small_sep.join(value_list)
        else:
            value_text = value
        return value_text
