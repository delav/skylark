from application.common.reader.builder.basebuilder import BaseBuilder
from application.common.reader.basereader import BaseReader
from application.common.reader.builder import CaseBuilder
from application.common.reader.builder import LibraryBuilder
from application.common.reader.builder import ScalarBuilder
from application.suitedir.models import SuiteDir


class MultiResource(BaseReader):
    def __init__(self, project_id, project_name):
        self.project_id = project_id
        self.project_name = project_name
        self.setting_str = ''
        self.data_map = self._handle_data()

    def _splice_resource(self, res_path):
        """
        splice to robot resource string
        :return: string
        """
        return self._splice_str('Resource', res_path)

    def setting_info(self):
        return self.setting_str

    def resources_map(self):
        return self.data_map

    def _handle_data(self):
        data_map = {}
        resource_builder = BaseResource(self.project_name)
        resource_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            category=1,
            parent_dir=None
        )
        if resource_queryset.exists():
            data = self._handle_dir(resource_queryset)
            for parent_path, suite_obj in data.items():
                path = resource_builder.resource_path(parent_path, suite_obj)

                text = ''
                text += self._settings_line
                text += resource_builder.get_resource_settings()
                text += self._variables_line
                text += resource_builder.get_resource_variables(suite_obj)
                text += self._keywords_line
                text += resource_builder.get_resource_keywords(suite_obj)

                data_map[path] = text
                self.setting_str += self._splice_resource(path)
        return data_map

    def _handle_dir(self, obj_iterator, result=None):
        if result is None:
            result = {}
        for obj in obj_iterator.iterator():
            if obj.children is None:
                pass
            else:
                return self._handle_dir(obj.children, result)
        return result


class BaseResource(BaseBuilder):
    """
    customize resource(keyword/case)
    """
    def __init__(self, project_name):
        self.project_name = project_name

    def get_resource_settings(self):
        settings_str = ''
        library_str = LibraryBuilder().setting_info()
        if library_str:
            settings_str += library_str
        settings_str += self.linefeed
        return settings_str

    def get_resource_variables(self, suite_obj):
        module_type = 2
        variables_str = ''
        scalar_str = ScalarBuilder(suite_obj.id, module_type).variable_info()
        if scalar_str:
            variables_str += scalar_str
        variables_str += self.linefeed
        return variables_str

    def get_resource_keywords(self, suite_obj):
        keywords_str = ''
        case_str = CaseBuilder().get_case_by_suite(suite_obj)
        if case_str:
            keywords_str += case_str
        keywords_str += self.linefeed
        return keywords_str

    def resource_path(self, suite_path, suite_obj):
        resource_name = suite_obj.suite_name
        return self.special_sep.join([suite_path, resource_name])

