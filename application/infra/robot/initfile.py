from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.variables import Variables
from application.infra.robot.assembler.settings import SetupTeardownSetting, ResourceSetting


class DirInitFile(object):
    """
    dir init file contain settings, variables
    """

    def __init__(self, test_setup, test_teardown, suite_setup,
                 suite_teardown, resource_list, variable_list):
        self.test_setup = test_setup
        self.test_teardown = test_teardown
        self.suite_setup = suite_setup
        self.suite_teardown = suite_teardown
        self.resource_list = resource_list
        self.variable_list = variable_list

    def get_text(self):
        config = Config()
        join_list = []
        setting_ctx = self._get_settings()
        if setting_ctx:
            settings_text = config.settings_line + setting_ctx
            join_list.append(settings_text)
        variable_ctx = self._get_variables()
        if variable_ctx:
            variable_text = config.variables_line + variable_ctx
            join_list.append(variable_text)
        return config.linefeed.join(join_list)

    def _get_setup_teardown_setting(self):
        return SetupTeardownSetting(
            self.test_setup,
            self.test_teardown,
            self.suite_setup,
            self.suite_teardown
        ).get_setup_teardown_setting()

    def _get_resources_setting(self):
        return ResourceSetting(self.resource_list).get_resource_setting()

    def _get_settings(self):
        return self._get_setup_teardown_setting() + self._get_resources_setting()

    def _get_variables(self):
        return Variables(self.variable_list).get_variables()