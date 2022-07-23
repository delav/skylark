from loguru import logger
from application.testsuite.models import TestSuite
from application.constant.models import Variable
from application.setupteardown.models import SetupTeardown
from application.infra.reader.builder.basebuilder import BaseBuilder


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
