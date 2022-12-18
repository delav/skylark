from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.settings import LibrarySetting
from application.infra.robot.assembler.variables import Variables, VariableKey
from application.infra.robot.assembler.testcase import KeywordAssembler, EntityKey


class ResourceFile(object):
    """
    resource file support library, variables, keywords(user customize keyword, similar with test case)
    """

    def __init__(self, library_list, variable_list, keyword_list):
        self.libraries = library_list
        self.variables = variable_list
        self.keywords = keyword_list

    def _get_libraries(self):
        return LibrarySetting(self.libraries).get_library_setting()

    def _get_variables(self):
        var_key = VariableKey(
            variable_name_key='name',
            variable_value_key='value'
        )
        return Variables(self.variables, var_key).get_variables()

    def _get_keywords(self):
        """
        these keywords actually is customized test cases
        """
        result = ''
        entity_key = EntityKey(
            keyword_name_key='keyword_name',
            keyword_input_key='keyword_input',
            keyword_output_key='keyword_output'
        )
        for item in self.keywords:
            result += KeywordAssembler(
                keyword_name=item['name'],
                keyword_inputs=item['inputs'],
                keyword_outputs=item['outputs'],
                entity_list=item['entity'],
                entity_key=entity_key
            ).get_keyword_content()
        return result

    def get_path(self):
        pass

    def get_text(self):
        config = Config()
        settings_text = config.settings_line + self._get_libraries()
        variable_text = config.variables_line + self._get_variables()
        keyword_text = config.keywords_line + self._get_keywords()
        return config.linefeed.join([settings_text, variable_text, keyword_text])



