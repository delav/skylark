from application.virtualfile.models import VirtualFile
from application.infra.robot.variablefile import VariablePyFile


class FileReader(object):

    def __init__(self, env_id, region_id, suite_id):
        self.env_id = env_id
        self.region_id = region_id
        self.suite_id = suite_id

    def read(self):
        return VariablePyFile(
            self._get_file_text()
        ).get_text()

    def _get_file_text(self):
        file_queryset = VirtualFile.objects.filter(
            env_id=self.env_id,
            region_id=self.region_id,
            test_suite__id=self.suite_id,
        )
        if not file_queryset.exists():
            return ''
        return file_queryset.first().file_text

