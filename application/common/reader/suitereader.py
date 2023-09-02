from django.conf import settings
from application.variable.models import Variable
from application.setupteardown.models import SetupTeardown
from application.tag.models import Tag
from application.common.reader.module.testcase import CaseReader
from application.common.reader.module.fixture import FixtureManager
from infra.robot.suitefile import SuiteFile
from infra.constant.constants import VARIABLE_NAME_KEY, VARIABLE_VALUE_KEY


class JsonSuiteReader(object):
    lib_path = settings.LIB_PATH

    def __init__(self, setup_teardown_data, suite_timeout, variable_list,
                 resource_list, variable_files, tag_list, case_data, include_cases):
        self.head_text_str = ''
        self.body_text_list = []
        self.file_text = ''
        self.setup_teardown_data = setup_teardown_data
        self.suite_timeout = suite_timeout
        self.variable_list = variable_list
        self.resource_list = resource_list
        self.variable_files = variable_files
        self.tag_list = tag_list
        self.case_data = case_data
        self.include_cases = include_cases

    def read(self):
        # not need tag for run now
        self.tag_list = []
        setup_teardown_data = self._get_setup_teardown()
        file = SuiteFile(
            setup_teardown_data[0],
            setup_teardown_data[1],
            setup_teardown_data[2],
            setup_teardown_data[3],
            self.suite_timeout,
            self.variable_list,
            self.resource_list,
            self.variable_files,
            self.tag_list,
            self._get_testcase_list()
        )
        self.file_text = file.get_text()
        self.head_text_str = file.get_head()
        self.body_text_list = file.get_body()
        return self.file_text

    def _get_testcase_list(self):
        return CaseReader(self.include_cases).get_by_case_data(self.case_data)

    def _get_setup_teardown(self):
        fixture_list = [
            self.setup_teardown_data.get('test_setup', ''),
            self.setup_teardown_data.get('test_teardown', ''),
            self.setup_teardown_data.get('suite_setup', ''),
            self.setup_teardown_data.get('suite_teardown', '')
        ]
        fixture_manager = FixtureManager(fixture_list)
        fixture_manager.replace_fixture_names()
        return fixture_manager.get_new_fixtures()


class DBSuiteReader(object):
    lib_path = settings.LIB_PATH

    def __init__(self, suite_id, module_type, suite_timeout, resource_list, variable_files):
        self.head_text_str = ''
        self.body_text_list = []
        self.file_text = ''
        self.suite_id = suite_id
        self.module_type = module_type
        self.suite_timeout = suite_timeout
        self.resource_list = resource_list
        self.variable_files = variable_files

    def read(self):
        setup_teardown_data = self._get_setup_teardown()
        file = SuiteFile(
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
        )
        file_text = file.get_text()
        self.head_text_str = file.get_head()
        self.body_text_list = file.get_body()
        return file_text

    def _get_setup_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return ['', '', '', '']
        setup_teardown = st_queryset.first()
        fixture_list = [
            setup_teardown.test_setup,
            setup_teardown.test_teardown,
            setup_teardown.suite_setup,
            setup_teardown.suite_teardown
        ]
        fixture_manager = FixtureManager(fixture_list)
        fixture_manager.replace_fixture_names()
        return fixture_manager.get_new_fixtures()

    def _get_tag_list(self):
        return []
        # tag_queryset = Tag.objects.filter(
        #     module_id=self.suite_id,
        #     module_type=self.module_type
        # )
        # return [t.name for t in tag_queryset.iterator()]

    def _get_variable_list(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({
                VARIABLE_NAME_KEY: item.name, VARIABLE_VALUE_KEY: item.value
            })
        return variable_list

    def _get_testcase_list(self):
        cases = CaseReader().get_by_suite_id(self.suite_id)
        return cases
