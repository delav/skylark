from infra.robot.assembler.setting import LibrarySetting, ResourceSetting, VariableSetting
from infra.robot.assembler.variable import VariableAssembler
from infra.robot.assembler.testcase import KeywordAssembler
from infra.robot.basefile import BaseFile
from infra.constant.constants import ENTITY_KEY


class ResourceKeywordFile(BaseFile):
    """
    resource file support library, variables, keywords(user customize keyword, similar with test case)
    """

    def __init__(self, resource_list, variable_files, variable_list, keyword_list):
        self.resources = resource_list
        self.varfiles = variable_files
        self.variables = variable_list
        self.keywords = keyword_list

    def _get_resources_setting(self):
        """
        this resource setting means only common variable files
        """
        return ResourceSetting(self.resources).get_resource_setting()

    def _get_variable_setting(self):
        return VariableSetting(self.varfiles).get_variable_setting()

    def _get_settings(self):
        """
        [*** Settings ***] filed content
        """
        return self._get_variable_setting() + self._get_resources_setting()

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        return VariableAssembler(self.variables).get_variables()

    def _get_keywords(self):
        """
        [*** Keywords ***] filed content, these keywords actually is customized test cases
        item is test case model dict, include entities
        """
        result = ''

        for item in self.keywords:
            result += KeywordAssembler(
                keyword_name=item.get('name'),
                keyword_inputs=item.get('inputs'),
                keyword_outputs=item.get('outputs'),
                entity_list=item.get(ENTITY_KEY)
            ).get_keyword_content()
        return result


class ResourceCommonFile(BaseFile):
    """
    common variables, separate file, scalar, will be used by all keyword resource or suite .
    import all library at here, and no longer needed import at every suite or keyword resource
    """

    def __init__(self, library_list, variable_list):
        self.libraries = library_list
        self.variables = variable_list

    def _get_library_setting(self):
        return LibrarySetting(self.libraries).get_library_setting()

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        return VariableAssembler(self.variables).get_variables()

    def _get_settings(self):
        """
        [*** Settings ***] filed content
        """
        return self._get_library_setting()

