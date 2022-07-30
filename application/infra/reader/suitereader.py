from application.infra.reader.basereader import BaseReader
from application.infra.reader.builder import *
from application.testsuite.models import TestSuite
from application.variable.models import Variable
from application.setupteardown.models import SetupTeardown


class SuiteReader(BaseReader):
    def __init__(self, project_id, project_name, module_id, module_type, env='test'):
        self.env = env
        self.project_id = project_id
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type

    def read(self):
        return {self._get_path(): self._get_text()}

    def _get_path(self):
        pass

    def _get_text(self):
        return self.head() + self.linefeed + self.body()

    def head(self):
        sh = SuiteHeader(self.project_id, self.project_name, self.module_id, self.module_type)
        settings_str = self._settings_line

        set_tear_str = sh.get_setup_and_teardown()
        if set_tear_str:
            settings_str += set_tear_str

        library_str = sh.get_library_info()
        settings_str += library_str

        resource_str = sh.get_resource_info()
        if resource_str:
            settings_str += resource_str

        variables_str = self._variables_line
        scalar_str = sh.get_suite_variables()
        if scalar_str:
            variables_str += scalar_str
        header_str = settings_str + self.linefeed + variables_str
        return header_str

    def body(self):
        case_str = CaseBuilder().get_case_by_ids()
        body_str = self._testcases_line + case_str
        return body_str


class SuiteHeader(BaseReader):
    def __init__(self, project_id, project_name, module_id, module_type):
        self.project_id = project_id
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
        st_str = SetTearBuilder(self.module_id, self.module_type).setting_info()
        return st_str

    def get_suite_variables(self):
        var_queryset = Variable.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not var_queryset.exists():
            return None
        var_str = VariableBuilder(self.project_name, self.module_id, self.module_type).setting_info()
        return var_str

    def get_library_info(self):
        return LibraryBuilder().setting_info()

    def get_resource_info(self):
        return MultiResource(self.project_id, self.project_name).setting_info()
