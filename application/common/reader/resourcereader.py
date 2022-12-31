import os
from application.pythonlib.models import PythonLib
from application.variable.models import Variable
from application.userkeyword.models import UserKeyword
from application.caseentity.models import CaseEntity
from application.infra.robot.resourcefile import ResourceFile
from application.common.reader.keywords import LibKeywordMap
from application.infra.settings import ENTITY_NAME_KEY, ENTITY_PARAMS_KEY, ENTITY_RETURN_KEY

lib_path = ''


class ResourceReader(object):

    keyword_dict = {}

    def __init__(self, env, project_id, suite_id, module_type):
        self.env = env
        self.project_id = project_id
        self.suite_id = suite_id
        self.module_type = module_type
        self.keyword_dict = LibKeywordMap().change_to_dict()

    def read(self):
        return self._fetch_content()

    def _fetch_content(self):
        return ResourceFile(
            self._get_library_list(),
            self._get_variable_list(),
            self._get_keyword_list()
        ).get_text()

    def _get_library_list(self):
        library_list = []
        pl_queryset = PythonLib.objects.all()
        for item in pl_queryset.iterator():
            if item['lib_type'] == 1:
                # builtin library
                library = item['lib_name']
            else:
                # customize python file
                library = os.path.join(lib_path, item['lib_name'])
            library_list.append(library)
        return library_list

    def _get_variable_list(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            env__env_name=self.env,
            module_id=self.suite_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item['name'], 'value': item['value']})
        return variable_list

    def _get_keyword_list(self):
        keyword_list = []
        kw_queryset = UserKeyword.objects.filter(
            project_id=self.project_id
        ).select_related('test_case')
        for item in kw_queryset.iterator():
            entity_list = []
            case_id = item.test_case.id
            entity_queryset = CaseEntity.objects.filter(test_case_id=case_id).order_by('seq_number')
            for entity in entity_queryset.iterator():
                entity_list.append({
                    ENTITY_NAME_KEY: self.keyword_dict[entity.keyword_id]['name'],
                    ENTITY_PARAMS_KEY: entity.input_args,
                    ENTITY_RETURN_KEY: entity.output_args
                })
            keyword_info = {
                'name': item.test_case.name,
                'inputs': item.test_case.inputs,
                'outputs': item.test_case.outputs,
                'entity': entity_list
            }
            keyword_list.append(keyword_info)
        return keyword_list
