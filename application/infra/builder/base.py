

class BaseBuilder(object):

    large_sep = ' ' * 8
    small_sep = ' ' * 4
    linefeed = '\n'
    special_sep = '#@#'

    def _splice_str(self, *args):
        """
        splice parameters to string
        :param args:
        :return: str
        """
        return self.large_sep.join(args).replace('\\', '/') + self.linefeed

    @property
    def _setting_line(self):
        """
        get the setting identification line
        :return: str
        """
        return '*** Settings ***' + self.linefeed

    @property
    def _variable_line(self):
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
    def _testcase_line(self):
        """
        get the testcase identification line
        :return:
        """
        return '*** Test Cases ***' + self.linefeed
