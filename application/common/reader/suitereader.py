from django.conf import settings
from application.variable.models import Variable
from application.setupteardown.models import SetupTeardown
from application.tag.models import Tag
from application.infra.robot.suitefile import SuiteFile
from application.common.reader.module.testcase import CaseReader


class JsonSuiteReader(object):
    lib_path = settings.LIB_PATH

    def __init__(self, setup_teardown_data, suite_timeout,
                 variable_list, resource_list, variable_files, tag_list, case_data):
        self.setup_teardown_data = setup_teardown_data
        self.suite_timeout = suite_timeout
        self.variable_list = variable_list
        self.resource_list = resource_list
        self.variable_files = variable_files
        self.tag_list = tag_list
        self.case_data = case_data

    def read(self):
        return SuiteFile(
            self.setup_teardown_data.get('test_setup', ''),
            self.setup_teardown_data.get('test_teardown', ''),
            self.setup_teardown_data.get('suite_setup', ''),
            self.setup_teardown_data.get('suite_teardown', ''),
            self.suite_timeout,
            self.variable_list,
            self.resource_list,
            self.variable_files,
            self.tag_list,
            self._get_testcase_list()
        ).get_text()

    def _get_testcase_list(self):
        cases = CaseReader().get_by_case_data(self.case_data)
        self.suite_cases = len(cases)
        return cases

    def get_suite_cases(self):
        return self.suite_cases or 0


class DBSuiteReader(object):
    lib_path = settings.LIB_PATH

    def __init__(self, suite_id, module_type, suite_timeout, resource_list, variable_files):
        self.suite_id = suite_id
        self.module_type = module_type
        self.suite_timeout = suite_timeout
        self.resource_list = resource_list
        self.variable_files = variable_files

    def read(self):
        setup_teardown_data = self._get_setup_teardown()
        return SuiteFile(
            setup_teardown_data[0],
            setup_teardown_data[1],
            setup_teardown_data[2],
            setup_teardown_data[3],
            self.suite_timeout,
            self._get_variable_list(),
            self.resource_list,
            self.variable_files,
            self._get_tag_list(),
            self._get_testcase_list()
        ).get_text()

    def _get_setup_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return ['', '', '', '']
        setup_teardown = st_queryset.first()
        return [
            setup_teardown.test_setup,
            setup_teardown.test_teardown,
            setup_teardown.suite_setup,
            setup_teardown.suite_teardown
        ]

    def _get_tag_list(self):
        tag_queryset = Tag.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        return [t.name for t in tag_queryset.iterator()]

    def _get_variable_list(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item.name, 'value': item.value})
        return variable_list

    def _get_testcase_list(self):
        cases = CaseReader().get_by_suite_id(self.suite_id)
        self.suite_cases = len(cases)
        return cases

    def get_suite_cases(self):
        return self.suite_cases or 0
