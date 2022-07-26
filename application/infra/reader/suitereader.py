from application.infra.reader.builder.basebuilder import BaseBuilder
from application.infra.reader.builder import *
from application.testsuite.models import TestSuite
from application.suitedir.models import SuiteDir
from application.variable.models import Variable
from application.setupteardown.models import SetupTeardown


class SuiteReader(BaseBuilder):
    def __init__(self, project_name, module_id, module_type):
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type

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


class SuiteHeader(BaseBuilder):
    def __init__(self, project_name, module_id, module_type):
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type

    def get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        st_str = SetTearBuilder().get_from_queryset(st_queryset)
        return st_str

    def get_suite_variables(self):
        var_queryset = Variable.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not var_queryset.exists():
            return None
        var_str = VariableBuilder(self.project_name).get_from_queryset(var_queryset)
        return var_str

    def get_library_info(self):
        return LibraryBuilder().get_path()

    def get_resource_info(self):
        pass