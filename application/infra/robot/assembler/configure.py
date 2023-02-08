import platform


class Config(object):
    __instance = None

    large_sep = ' ' * 8
    small_sep = ' ' * 4
    linefeed = '\n'

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        _sys = platform.system()
        if _sys == 'Windows':
            line_feed = '\r\n'
        elif _sys == "Linux":
            line_feed = '\n'
        elif _sys == 'MacOS':
            line_feed = '\r'
        else:
            line_feed = '\n'
        self.linefeed = line_feed

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
