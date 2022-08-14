import os
from django.conf import settings
from application.common.reader.builder.basebuilder import BaseBuilder
from application.pythonlib.models import PythonLib


class LibraryBuilder(BaseBuilder):
    """
    project common import library
    """

    def __init__(self):
        self.builtin_lib_list = settings.BUILTIN_LIB
        self.customize_path = settings.BASE_DIR + settings.LIB_URL

    def _handle_customize_path(self, file_name):
        if not file_name.endswith('.py'):
            file_name += '.py'
        full_path = os.path.join(self.customize_path, file_name)
        if not os.path.isfile(full_path):
            return ''
        return full_path

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

    def setting_info(self):
        lib_str = ''
        lib_queryset = PythonLib.objects.all()
        if not lib_queryset.exists():
            return lib_str
        for obj in lib_queryset.iterator():
            path = ''
            if obj.lib_type == 1:
                path = obj.lib_name
            elif obj.lib_type == 2:
                path = self._handle_customize_path(obj.lib_name)
            lib_str += self._splice_library_str(path)
        return lib_str

