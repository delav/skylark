import os
from django.conf import settings
from application.pythonlib.models import PythonLib
from application.variable.models import Variable
from application.userkeyword.models import UserKeyword
from application.infra.robot.resourcefile import ResourceKeywordFile, ResourceCommonFile
from application.common.reader.module.testcase import CaseReader


class ResourceKeywordReader(object):

    def __init__(self, suite_id, module_type, resource_list, variable_files):
        self.suite_id = suite_id
        self.module_type = module_type
        self.resource_list = resource_list
        self.variable_files = variable_files

    def read(self):
        return ResourceKeywordFile(
            self.resource_list,
            self.variable_files,
            self._get_variable_list(),
            self._get_keyword_list()
        ).get_text()

    def _get_variable_list(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            module_id=self.suite_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item['name'], 'value': item['value']})
        return variable_list

    def _get_keyword_list(self):
        return CaseReader().get_by_suite_id(self.suite_id)


class ResourceCommonReader(object):
    lib_path = settings.LIB_PATH

    def __init__(self, env_id, region_id, project_id, module_type):
        self.env_id = env_id
        self.region_id = region_id
        self.project_id = project_id
        self.module_type = module_type

    def read(self):
        return ResourceCommonFile(
            self._get_library_list(),
            self._get_variable_list()
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
                library = os.path.join(self.lib_path, item['lib_name'])
            library_list.append(library)
        return library_list

    def _get_variable_list(self):
        variable_list, name_dict = self._get_non_region_variables()
        if self.region_id is not None:
            return variable_list
        var_queryset = Variable.objects.filter(
            env_id=self.env_id,
            region_id=self.region_id,
            module_id=self.project_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            var = {'name': item.name, 'value': item.value}
            if item.name in name_dict:
                repeat_index = name_dict[item.name]
                variable_list[repeat_index] = var
            else:
                variable_list.append(var)
        return variable_list

    def _get_non_region_variables(self):
        variable_name_map = {}
        non_region_variable_list = []
        non_region_variable = Variable.objects.filter(
            env_id=self.env_id,
            region_id=None,
            module_id=self.project_id,
            module_type=self.module_type
        )
        index = 0
        for item in non_region_variable.iterator():
            var = {'name': item.name, 'value': item.value}
            non_region_variable_list.append(var)
            variable_name_map[item.name] = index
            index += 1
        return non_region_variable_list, variable_name_map
