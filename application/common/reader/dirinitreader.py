from application.common.reader.builder import SetTearBuilder
from application.setupteardown.models import SetupTeardown
from application.suitedir.models import SuiteDir
from application.common.reader.basereader import BaseReader


class DirInitReader(BaseReader):

    def __init__(self, project_name, module_id, module_type):
        super(DirInitReader, self).__init__()
        self.module_id = module_id
        self.module_type = module_type
        self.project_name = project_name

    def read(self):
        text = self._get_setup_and_teardown()
        if not text:
            return {}
        text = self._settings_line + text
        return {self._get_path(): text}

    def _get_path(self):
        dir_obj = SuiteDir.objects.get(id=self.module_id)
        dir_path = self._recursion_dir(dir_obj, [dir_obj.dir_name])
        path_list = dir_path.append(self.project_name)
        return self.special_sep.join(path_list[::-1])

    def _get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        return SetTearBuilder(self.module_id, self.module_type).setting_info()

    def _recursion_dir(self, obj, path_list):
        if obj.parent_dir is None:
            return path_list
        path_list.append(obj.parent_dir.dir_name)
        return self._recursion_dir(obj.parent_dir, path_list)
