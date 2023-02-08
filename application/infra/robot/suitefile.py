from application.infra.robot.assembler.setting import ResourceSetting, VariableSetting, TagSetting
from application.infra.robot.assembler.setting import SetupTeardownSetting, TimeoutSetting
from application.infra.robot.assembler.variable import VariableAssembler
from application.infra.robot.assembler.testcase import TestcaseAssembler
from application.infra.robot.basefile import BaseFile
from application.infra.robot.assembler.configure import Config


class SuiteFile(BaseFile):
    """
    suite file, contain settings, variables, testcases
    """

    def __init__(self, test_setup, test_teardown, suite_setup, suite_teardown,
                 suite_timeout, variable_list, resource_list, variable_files, tag_list, testcase_list):
        self.test_setup = test_setup
        self.test_teardown = test_teardown
        self.suite_setup = suite_setup
        self.suite_teardown = suite_teardown
        self.suite_timeout = suite_timeout
        self.variables = variable_list
        self.resources = resource_list
        self.varfiles = variable_files
        self.tag_list = tag_list
        self.testcases = testcase_list
        self.header_text = ''
        self.case_text_list = []

    def _get_setup_teardown_setting(self):
        return SetupTeardownSetting(
            self.test_setup,
            self.test_teardown,
            self.suite_setup,
            self.suite_teardown
        ).get_setup_teardown_setting()

    def _get_timeout_setting(self):
        return TimeoutSetting(self.suite_timeout).get_timeout_setting()

    def _get_resources_setting(self):
        return ResourceSetting(self.resources).get_resource_setting()

    def _get_tags_setting(self):
        return TagSetting(self.tag_list).get_tag_setting()

    def _get_variable_setting(self):
        return VariableSetting(self.varfiles).get_variable_setting()

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        return VariableAssembler(self.variables).get_variables()

    def _get_testcases(self):
        """
        [*** Test Cases ***] filed content
        """
        result = ''
        for item in self.testcases:
            case_text = TestcaseAssembler(
                case_name=item['name'],
                case_id=item['id'],
                case_timeout=item['timeout'],
                entity_list=item['entity']
            ).get_case_content()
            result += case_text
            self.case_text_list.append(case_text)
        return result

    def _get_settings(self):
        """
        [*** Settings ***] filed content
        """
        return self._get_setup_teardown_setting() + self._get_timeout_setting() + \
            self._get_resources_setting() + self._get_variable_setting() + self._get_tags_setting()

    def get_text(self):
        config = Config()
        head_ctx_tuple = (
            (config.settings_line, self._get_settings()),
            (config.variables_line, self._get_variables()),
        )
        body_ctx_tuple = (
            (config.keywords_line, self._get_keywords),
            (config.testcases_line, self._get_testcases()),
        )
        header_list = []
        section_list = []
        for line, text in head_ctx_tuple:
            if not text:
                continue
            header_list.append(line + text)
            section_list.append(line + text)
        for line, text in body_ctx_tuple:
            if not text:
                continue
            section_list.append(line + text)
        self.header_text = config.linefeed.join(header_list)
        return config.linefeed.join(section_list)

    def get_head(self):
        return self.header_text

    def get_body(self):
        return self.case_text_list

