import os
from django.conf import settings
from application.infra.reader.builder.basebuilder import BaseBuilder


class LibraryBuilder(BaseBuilder):
    """
    project common import library
    """

    def __init__(self):
        super(LibraryBuilder, self).__init__()
        self.builtin_lib_list = settings.BUILTIN_LIB
        self.customize_path = settings.BASE_DIR + settings.LIB_URL

    def _splice_library_str(self, *args):
        """
        splice to robot library string
        :param args: splice parameter
        :return: str
        """
        return self._splice_str('Library', *args)

    def _get_builtin_library(self):
        """
        get settings builtin library
        eg: RequestsLibrary, Collections ...
        :return: builtin library str
        """
        builtin_lib_str = ''
        for b_lib in self.builtin_lib_list:
            builtin_lib_str += self._splice_library_str(b_lib)
        return builtin_lib_str

    def _get_customize_library(self):
        """
        get user customized python library
        :return: customize library str
        """
        customize_lib_str = ''
        lib_file = os.listdir(self.customize_path)
        for f in lib_file:
            if f.endswith('.py'):
                full_path = os.path.join(self.customize_path, f)
                customize_lib_str += self._splice_library_str(full_path)
        return customize_lib_str

    def get_library_info(self):
        return self._get_builtin_library() + self._get_customize_library()