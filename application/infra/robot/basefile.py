from application.infra.robot.assembler.configure import Config


class BaseFile(object):
    """
    base file sections
    """

    def get_text(self):
        config = Config()
        ctx_tuple = (
            (config.settings_line, self._get_settings()),
            (config.variables_line, self._get_variables()),
            (config.keywords_line, self._get_keywords),
            (config.testcases_line, self._get_testcases()),
        )
        section_list = []
        for line, text in ctx_tuple:
            if not text:
                continue
            section_list.append(line + text)
        return config.linefeed.join(section_list)

    def _get_settings(self):
        """
        [*** Settings ***] filed content
        """
        pass

    def _get_variables(self):
        """
        [*** Variables ***] filed content
        """
        pass

    def _get_keywords(self):
        """
        [*** Keywords ***] filed content
        """
        pass

    def _get_testcases(self):
        """
        [*** Test Cases ***] filed content
        """
        pass
