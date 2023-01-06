import os
from application.pythonlib.models import PythonLib
from application.variable.models import Variable
from application.setupteardown.models import SetupTeardown
from application.testcase.models import TestCase
from application.caseentity.models import CaseEntity
from application.infra.robot.suitefile import SuiteFile
from application.common.reader.keywords import LibKeywordMap
from application.infra.settings import ENTITY_NAME_KEY, ENTITY_PARAMS_KEY, ENTITY_RETURN_KEY

lib_path = ''


class SuiteReader(object):

    keyword_dict = {}

    def __init__(self, project_id, project_name, suite_id, module_type, suite_timeout, resource_list):
        self.project_id = project_id
        self.project_name = project_name
        self.suite_id = suite_id
        self.module_type = module_type
        self.suite_timeout = suite_timeout
        self.resource_list = resource_list
        self.keyword_dict = LibKeywordMap().change_to_dict()

    def read(self):
        return self._fetch_content()

    def _fetch_content(self):
        st_list = self._get_setup_teardown()
        return SuiteFile(
            st_list[0],
            st_list[1],
            st_list[2],
            st_list[3],
            self.suite_timeout,
            self._get_library_list(),
            self._get_variable_list(),
            self._get_resource_list(),
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

    def _get_library_list(self):
        library_list = []
        pl_queryset = PythonLib.objects.all()
        for item in pl_queryset.iterator():
            if item.lib_type == 1:
                # builtin library
                library = item.lib_name
            else:
                # customize python file
                library = os.path.join(lib_path, item.lib_name)
            library_list.append(library)
        return library_list

    def _get_variable_list(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item.name, 'value': item.value})
        return variable_list

    def _get_resource_list(self):
        return self.resource_list

    def _get_testcase_list(self):
        testcase_list = []
        case_queryset = TestCase.objects.filter(
            test_suite_id=self.suite_id
        )
        for item in case_queryset.iterator():
            entity_list = []
            entity_queryset = CaseEntity.objects.filter(
                test_case_id=item.id
            ).order_by('seq_number')
            for entity in entity_queryset.iterator():
                entity_list.append({
                    ENTITY_NAME_KEY: self.keyword_dict[entity.keyword_id]['name'],
                    ENTITY_PARAMS_KEY: entity.input_args,
                    ENTITY_RETURN_KEY: entity.output_args
                })
            case_info = {
                'name': item.name,
                'inputs': item.inputs,
                'outputs': item.outputs,
                'timeout': item.timeout,
                'entity': entity_list
            }
            testcase_list.append(case_info)
        return testcase_list
