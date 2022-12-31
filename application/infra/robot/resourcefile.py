from application.infra.robot.assembler.config import Config
from application.infra.robot.assembler.settings import LibrarySetting
from application.infra.robot.assembler.variables import Variables
from application.infra.robot.assembler.testcase import KeywordAssembler


class ResourceFile(object):
    """
    resource file support library, variables, keywords(user customize keyword, similar with test case)
    """

    def __init__(self, library_list, variable_list, keyword_list):
        self.libraries = library_list
        self.variables = variable_list
        self.keywords = keyword_list

    def _get_libraries_setting(self):
        return LibrarySetting(self.libraries).get_library_setting()

    def _get_settings(self):
        return self._get_libraries_setting()

    def _get_variables(self):
        return Variables(self.variables).get_variables()

    def _get_keywords(self):
        """
        these keywords actually is customized test cases
        """
        result = ''

        for item in self.keywords:
            result += KeywordAssembler(
                keyword_name=item['name'],
                keyword_inputs=item['inputs'],
                keyword_outputs=item['outputs'],
                entity_list=item['entity']
            ).get_keyword_content()
        return result

    def get_path(self):
        pass

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
        keyword_ctx = self._get_keywords()
        if keyword_ctx:
            keyword_text = config.keywords_line + keyword_ctx
            join_list.append(keyword_text)
        return config.linefeed.join(join_list)



