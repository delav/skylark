import platform


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

    @staticmethod
    def _sys_linefeed():
        _sys = platform.system()
        if _sys == 'Windows':
            line_feed = '\r\n'
        elif _sys == "Linux":
            line_feed = '\n'
        elif _sys == 'MacOS':
            line_feed = '\r'
        else:
            line_feed = '\n'
        return line_feed
