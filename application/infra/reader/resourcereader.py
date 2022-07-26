from application.infra.reader.builder.basebuilder import BaseBuilder
from application.suitedir.models import SuiteDir
from application.infra.reader.builder import ResourceBuilder


class ResourceReader(BaseBuilder):
    def __init__(self, project_id, project_name, module_id, module_type):
        self.project_id = project_id
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type
        self.data_map = self._handle_data()

    def get_path(self):
        pass

    def get_content(self):
        pass

    def _handle_data(self):
        resource_builder = ResourceBuilder(self.project_name)
        resource_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            dir_type=1,
            parent_dir=None
        )
        if not resource_queryset.exists():
            return {}
        data = self._handle_dir(resource_queryset)
        data_map = {}
        for path, suite_obj in data.items():
            key = resource_builder.setting_info(path, suite_obj)
            value = resource_builder.resource_text(suite_obj)
            data_map[key] = value
        return data_map

    def _handle_dir(self, obj_iterator, result=None):
        if result is None:
            result = []
        for obj in obj_iterator:
            if obj.children is None:
                result.append(obj)
            else:
                return self._handle_dir(obj.children, result)
        return {}