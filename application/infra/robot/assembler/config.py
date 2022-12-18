import platform


class Config(object):

    large_sep = ' ' * 8
    small_sep = ' ' * 4
    linefeed = '\n'
    special_sep = '#@#'

    def __new__(cls):
        _sys = platform.system()
        if _sys == 'Windows':
            line_feed = '\r\n'
        elif _sys == "Linux":
            line_feed = '\n'
        elif _sys == 'MacOS':
            line_feed = '\r'
        else:
            line_feed = '\n'
        cls.linefeed = line_feed

    @property
    def settings_line(self):
        """
        get the setting identification line
        :return: str
        """
        return '*** Settings ***' + self.linefeed

    @property
    def variables_line(self):
        """
        get the variable identification line
        :return: str
        """
        return '*** Variables ***' + self.linefeed

    @property
    def keywords_line(self):
        """
        get the keyword identification line
        :return:
        """
        return '*** Keywords ***' + self.linefeed

    @property
    def testcases_line(self):
        """
        get the testcase identification line
        :return:
        """
        return '*** Test Cases ***' + self.linefeed
