from infra.robot.assembler.variable import VariableAssembler
from infra.robot.assembler.setting import SetupTeardownSetting, ResourceSetting, TagSetting, VariableSetting
from infra.robot.basefile import BaseFile


class DirInitFile(BaseFile):
    """
    dir init file contain settings, variables(only use in setup or teardown)
    """

    def __init__(self, test_setup, test_teardown, suite_setup,
                 suite_teardown, resource_list, variable_files, tag_list, variable_list):
        self.test_setup = test_setup
        self.test_teardown = test_teardown
        self.suite_setup = suite_setup
        self.suite_teardown = suite_teardown
        self.resource_list = resource_list
        self.varfiles = variable_files
        self.tag_list = tag_list
        self.variable_list = variable_list

    def _get_setup_teardown_setting(self):
        return SetupTeardownSetting(
            self.test_setup,
            self.test_teardown,
            self.suite_setup,
            self.suite_teardown
        ).get_setup_teardown_setting()

    def _get_resources_setting(self):
        return ResourceSetting(self.resource_list).get_resource_setting()

    def _get_variable_setting(self):
        return VariableSetting(self.varfiles).get_variable_setting()

    def _get_tags_setting(self):
        return TagSetting(self.tag_list).get_tag_setting()

    def _get_settings(self):
        """
        [*** Settings ***] filed content
        """
        return self._get_setup_teardown_setting() + self._get_resources_setting() + \
            self._get_variable_setting() + self._get_tags_setting()

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        return VariableAssembler(self.variable_list).get_variables()
