from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.settings import LibrarySetting, ResourceSetting, SetupTeardownSetting
from application.infra.robot.assembler.variables import Variables, VariableKey
from application.infra.robot.assembler.testcase import TestcaseAssembler, EntityKey


class SuiteFile(object):
    """
    suite file, contain settings, variables, testcases
    """

    def __init__(self, test_setup, test_teardown, suite_setup, suite_teardown,
                 library_list, variable_list, keyword_list, resource_list):
        self.test_setup = test_setup
        self.test_teardown = test_teardown
        self.suite_setup = suite_setup
        self.suite_teardown = suite_teardown
        self.libraries = library_list
        self.variables = variable_list
        self.keywords = keyword_list
        self.resources = resource_list

    def _get_setup_teardown(self):
        return SetupTeardownSetting(
            self.test_setup,
            self.test_teardown,
            self.suite_setup,
            self.suite_teardown
        ).get_setup_teardown_setting()

    def _get_libraries(self):
        return LibrarySetting(self.libraries).get_library_setting()

    def _get_resources(self):
        return ResourceSetting(self.resources).get_resource_setting()

    def _get_variables(self):
        var_key = VariableKey(
            variable_name_key='name',
            variable_value_key='value'
        )
        return Variables(self.variables, var_key).get_variables()

    def _get_testcases(self):
        """
        these keywords actually is customized test cases
        """
        result = ''
        entity_key = EntityKey(
            keyword_name_key='name',
            keyword_input_key='inputs',
            keyword_output_key='outputs'
        )
        for item in self.keywords:
            result += TestcaseAssembler(
                case_name=item['name'],
                case_timeout=item['timeout'],
                entity_list=item['entity'],
                entity_key=entity_key
            ).get_case_content()
        return result

    def get_path(self):
        pass

    def get_text(self):
        config = Config()
        settings_text = config.settings_line + self._get_setup_teardown() + self._get_libraries() + self._get_resources()
        variable_text = config.variables_line + self._get_variables()
        keyword_text = config.tesecase_line + self._get_testcases()
        return config.linefeed.join([settings_text, variable_text, keyword_text])




