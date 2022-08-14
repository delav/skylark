from application.common.reader.builder.basebuilder import BaseBuilder


class BaseReader(BaseBuilder):

    @property
    def _settings_line(self):
        """
        get the setting identification line
        :return: str
        """
        return '*** Settings ***' + self.linefeed

    @property
    def _variables_line(self):
        """
        get the variable identification line
        :return: str
        """
        return '*** Variables ***' + self.linefeed

    @property
    def _keywords_line(self):
        """
        get the keyword identification line
        :return:
        """
        return '*** Keywords ***' + self.linefeed

    @property
    def _testcases_line(self):
        """
        get the testcase identification line
        :return:
        """
        return '*** Test Cases ***' + self.linefeed

    def read(self):
        return {}
