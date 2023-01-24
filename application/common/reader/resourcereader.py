import os
from django.conf import settings
from application.pythonlib.models import PythonLib
from application.variable.models import Variable
from application.userkeyword.models import UserKeyword
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers
from application.infra.robot.resourcefile import ResourceFile
from application.common.reader.libkeywords import LibKeywordManager, LibKeywordMap
from application.infra.constant import ENTITY_NAME_KEY, ENTITY_PARAMS_KEY, ENTITY_RETURN_KEY


class ResourceReader(object):
    lib_path = settings.LIB_PATH

    def __init__(self, project_id, suite_id, module_type, resource_list, combine=False):
        self.project_id = project_id
        self.suite_id = suite_id
        self.module_type = module_type
        self.resource_list = resource_list
        self.combine = combine

    def read(self):
        return self._fetch_content()

    def _fetch_content(self):
        return ResourceFile(
            self._get_library_list(),
            self._get_variable_list(),
            self._get_resource_list(),
            self._get_keyword_list()
        ).get_text()

    def _get_resource_list(self):
        return self.resource_list

    def _get_library_list(self):
        library_list = []
        pl_queryset = PythonLib.objects.all()
        for item in pl_queryset.iterator():
            if item['lib_type'] == 1:
                # builtin library
                library = item['lib_name']
            else:
                # customize python file
                library = os.path.join(self.lib_path, item['lib_name'])
            library_list.append(library)
        return library_list

    def _get_variable_list(self):
        variable_list = []
        if self.combine:
            suite_id = self.suite_id
            if not isinstance(suite_id, list):
                suite_id = [suite_id]
            var_queryset = Variable.objects.filter(
                module_id__in=suite_id,
                module_type=self.module_type
            )
        else:
            var_queryset = Variable.objects.filter(
                module_id=self.suite_id,
                module_type=self.module_type
            )
        for item in var_queryset.iterator():
            variable_list.append({'name': item['name'], 'value': item['value']})
        return variable_list

    def _get_keyword_list(self):
        customize_keyword_list = []
        if self.combine:
            kw_queryset = UserKeyword.objects.filter(
                project_id=self.project_id
            ).select_related('test_case')
        else:
            kw_queryset = UserKeyword.objects.filter(
                test_case__test_suite__id=self.suite_id
            ).select_related('test_case')
        map_instance = LibKeywordMap()
        for item in kw_queryset.iterator():
            entity_list = []
            case_id = item.test_case.id
            entity_queryset = CaseEntity.objects.filter(test_case_id=case_id).order_by('seq_number')
            for entity in entity_queryset.iterator():
                ser_entity = CaseEntitySerializers(entity).data
                info = LibKeywordManager(ser_entity, map_instance)
                entity_list.append({
                    ENTITY_NAME_KEY: info.keyword_name,
                    ENTITY_PARAMS_KEY: info.entity_input,
                    ENTITY_RETURN_KEY: info.entity_output
                })
            customize_keyword_info = {
                'name': item.test_case.name,
                'inputs': item.test_case.inputs,
                'outputs': item.test_case.outputs,
                'entity': entity_list
            }
            customize_keyword_list.append(customize_keyword_info)
        return customize_keyword_list

