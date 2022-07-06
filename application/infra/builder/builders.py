import os
from django.conf import settings
from loguru import logger
from application.testsuite.models import TestSuite
from application.variable.models import Variable
from application.setupteardown.models import SetupTeardown
from .base import BaseBuilder


class LibraryBuilder(BaseBuilder):

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

    def get_library(self):
        return self._get_builtin_library() + self._get_customize_library()


class SetTearBuilder(BaseBuilder):

    def __init__(self):
        super(SetTearBuilder, self).__init__()

    def _clear_spaces(self, value):
        return value.replace(' ', '')

    def _is_not_null(self, value):
        return value is not None and value != ''

    def _splice_settear(self, key, *args):
        return key + self.large_sep + self.small_sep.join(*args) + self.linefeed

    def _handler_step(self, step_str, prefix):
        module_setup_str = ''
        if self._is_not_null(step_str):
            if '|' in step_str:
                module_setup_list = step_str.split('|')
                if 'AND' in module_setup_list:
                    module_setup_list.insert(0, 'RUN KEYWORDS')
            else:
                module_setup_list = [step_str]
            module_setup_str = self._splice_settear(prefix, *module_setup_list)
        return module_setup_str

    def get_from_object(self, st_obj):
        setup_teardown_str = ''
        try:
            module_setup = self._clear_spaces(st_obj.module_setup)
            module_teardown = self._clear_spaces(st_obj.module_teardown)
            test_setup = self._clear_spaces(st_obj.test_setup)
            test_teardown = self._clear_spaces(st_obj.test_teardown)
        except (Exception,):
            return setup_teardown_str

        module_setup_str = self._handler_step(module_setup, 'Suite Setup')
        setup_teardown_str += module_setup_str

        module_teardown_str = self._handler_step(module_teardown, 'Suite Teardown')
        setup_teardown_str += module_teardown_str

        test_setup_str = self._handler_step(test_setup, 'Test Setup')
        setup_teardown_str += test_setup_str

        test_teardown_str = self._handler_step(test_teardown, 'Test Teardown')
        setup_teardown_str += test_teardown_str

        return setup_teardown_str


class VariableBuilder(BaseBuilder):
    """
    only deal with suite variable(scalar only on suite)
    """
    def __init__(self):
        super(VariableBuilder, self).__init__()

    def _splice_kv(self, key, value):
        return key + self.small_sep + value + self.linefeed

    def get_from_queryset(self, var_queryset):
        var_str = ''
        for obj in var_queryset.iterator():
            var_str += self._splice_kv(obj.name, obj.value)
        return var_str


class InitSuiteHeader(BaseBuilder):
    def __init__(self, module_id, module_type):
        super(InitSuiteHeader, self).__init__()
        self.module_id = module_id
        self.module_type = module_type

    def get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        obj = st_queryset.first()
        st_str = SetTearBuilder().get_from_object(obj)
        return st_str

    def get_variable(self):
        var_queryset = Variable.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        var_strs = VariableBuilder().get_from_queryset(var_queryset)
        return var_strs


class InitResourceHeader(BaseBuilder):
    def __init__(self, module_id, module_type):
        super(InitResourceHeader, self).__init__()
        self.module_id = module_id
        self.module_type = module_type


class SuiteHeaderBuilder(BaseBuilder):

    def __init__(self, project_id, project_name, module_id, module_type):
        self.module_id = module_id
        self.module_type = module_type
        self.project_id = project_id
        self.project_name = project_name

    def get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        obj = st_queryset.first()
        st_str = SetTearBuilder().get_from_object(obj)
        return st_str

    # def get_resource_path(self):
    #     rb = ResourceBuilder(self.project_id, self.project_name)
    #     common_resource = rb.get_common_resource()
    #     customize_resource = rb.get_customize_resource()
    #     return common_resource + customize_resource

    def get_variables(self):
        pass

    def add_suite_head_info(self, suite_id, suite_file, project_path):
        install_list = []
        st_list = self.get_file_setup_teardown(suite_id, 1)
        l_list = self.get_suite_library()
        r_list = self.get_suite_resource(project_path)
        install_list.extend(st_list)
        install_list.extend(l_list)
        install_list.extend(r_list)
        with open(suite_file, 'w+') as f:
            f.write('*** Settings ***' + self.linefeed)
            f.writelines(install_list)
            f.write(self.linefeed)
            f.flush()
        logger.info('测试套件文件头写入完成')

    def add_resource_head_info(self, suite_file, project_path):
        install_list = []
        l_list = self.get_suite_library()
        install_list.extend(l_list)
        e_str = 'Resource' + self.small_sep + project_path + self.common_path + self.env_file + self.linefeed
        g_str = 'Resource' + self.small_sep + project_path + self.common_path + self.global_file + self.linefeed
        install_list.append(e_str.replace('\\', '/'))
        install_list.append(g_str.replace('\\', '/'))
        with open(suite_file, 'w+') as f:
            f.write('*** Settings ***' + self.linefeed)
            f.writelines(install_list)
            f.write(self.linefeed)
            f.flush()
        logger.info('源文件头写入完成')

    def add_init_file_info(self, dir_id, init_file, d_type, project_path):
        install_list = []
        f_list = self.get_file_setup_teardown(dir_id, d_type)
        r_list = self.get_resource_keywords_file(project_path)
        install_list.extend(f_list)
        install_list.extend(r_list)
        if not install_list:
            return
        with open(init_file, 'w+') as f:
            f.write('*** Settings ***' + self.linefeed)
            f.writelines(install_list)
            f.write(self.linefeed)
            f.flush()
        logger.info('测试套件文件头写入完成')

    def add_suite_variables(self, suite_id, suite_file):
        var_list = []
        suite_obj = TestSuite.objects.get(id=suite_id)
        all_var = suite_obj.var_set.all()
        for var_item in all_var.iterator():
            var_name = var_item.name
            var_value = var_item.value
            var_desc = var_item.comment
            v_str = var_name + self.small_sep + var_value + self.small_sep + '# ' + var_desc + self.linefeed
            var_list.append(v_str.replace('\\', '/'))
        with open(suite_file, 'a+') as f:
            f.write('*** Variables ***' + self.linefeed)
            f.writelines(var_list)
            f.write(self.linefeed)
            f.flush()
        logger.info('测试套件变量写入完成')
