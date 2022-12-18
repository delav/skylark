from application.setupteardown.models import SetupTeardown
from application.infra.robot.initfile import DirInitFile


class DirInitReader(object):

    def __init__(self, path, module_id, module_type):
        self.path = path
        self.module_id = module_id
        self.module_type = module_type

    def read(self):
        text = self._fetch_setup_and_teardown()
        if not text:
            return {}
        return {self.path: text}

    def _fetch_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return ''
        obj = st_queryset.first()
        return DirInitFile(obj.test_setup, obj.suite_teardown, obj.suite_setup, obj.suite_teardown).get_text()

