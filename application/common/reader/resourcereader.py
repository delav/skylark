import os
from application.pythonlib.models import PythonLib
from application.variable.models import Variable
from application.userkeyword.models import UserKeyword
from application.caseentity.models import CaseEntity
from application.infra.robot.resourcefile import ResourceFile

lib_path = ''


class ResourceReader(object):

    keyword_dict = {}

    def __init__(self, env, path, project_id, module_id, module_type):
        self.env = env
        self.path = path
        self.project_id = project_id
        self.module_id = module_id
        self.module_type = module_type

    def read(self):
        return {self.path: self._fetch_content()}

    def _fetch_content(self):
        library_list = []
        variable_list = []
        keyword_list = []
        pl_queryset = PythonLib.objects.all()
        for item in pl_queryset.iterator():
            if item['lib_type'] == 1:
                # builtin library
                library = item['lib_name']
            else:
                # customize python file
                library = os.path.join(lib_path, item['lib_name'])
            library_list.append(library)
        var_queryset = Variable.objects.filter(
            env__env_name=self.env,
            module_id=self.module_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item['name'], 'value': item['value']})
        kw_queryset = UserKeyword.objects.filter(
            project_id=self.project_id
        ).select_related('test_case')
        for item in kw_queryset.iterator():
            entity_list = []
            entity_queryset = CaseEntity.objects.filter(test_case_id=item.id).order_by('seq_number')
            for entity in entity_queryset.iterator():
                entity_list.append({
                    'keyword_name': self.keyword_dict[entity['keyword_id']],
                    'keyword_input': entity['input_args'],
                    'keyword_output': entity['output_args']
                })
            keyword_info = {
                'name': item.test_case.name,
                'inputs': item.test_case.inputs,
                'outputs': item.test_case.outputs,
                'entity': entity_list
            }
            keyword_list.append(keyword_info)
        return ResourceFile(library_list, variable_list, keyword_list).get_text()
