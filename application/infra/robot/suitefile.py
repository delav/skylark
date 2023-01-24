from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.settings import LibrarySetting, ResourceSetting
from application.infra.robot.assembler.settings import SetupTeardownSetting, TimeoutSetting
from application.infra.robot.assembler.variables import Variables
from application.infra.robot.assembler.testcase import TestcaseAssembler


class SuiteFile(object):
    """
    suite file, contain settings, variables, testcases
    """

    def __init__(self, test_setup, test_teardown, suite_setup, suite_teardown,
                 suite_timeout, library_list, variable_list, resource_list, testcase_list):
        self.test_setup = test_setup
        self.test_teardown = test_teardown
        self.suite_setup = suite_setup
        self.suite_teardown = suite_teardown
        self.suite_timeout = suite_timeout
        self.libraries = library_list
        self.variables = variable_list
        self.resources = resource_list
        self.testcases = testcase_list

    def _get_setup_teardown_setting(self):
        return SetupTeardownSetting(
            self.test_setup,
            self.test_teardown,
            self.suite_setup,
            self.suite_teardown
        ).get_setup_teardown_setting()

    def _get_timeout_setting(self):
        return TimeoutSetting(self.suite_timeout).get_timeout_setting()

    def _get_libraries_setting(self):
        return LibrarySetting(self.libraries).get_library_setting()

    def _get_resources_setting(self):
        return ResourceSetting(self.resources).get_resource_setting()

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        return Variables(self.variables).get_variables()

    def _get_testcases(self):
        """
        [*** Test Cases ***] filed content
        """
        result = ''
        for item in self.testcases:
            result += TestcaseAssembler(
                case_name=item['name'],
                case_id=item['id'],
                case_timeout=item['timeout'],
                entity_list=item['entity']
            ).get_case_content()
        return result

    def _get_settings(self):
        """
        [*** Settings ***] filed content
        """
        return self._get_setup_teardown_setting() + self._get_timeout_setting() +\
            self._get_libraries_setting() + self._get_resources_setting()

    def get_text(self):
        """
        will return all suite file content
        """
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
        testcase_text = config.testcases_line + self._get_testcases()
        join_list.append(testcase_text)
        return config.linefeed.join(join_list)
