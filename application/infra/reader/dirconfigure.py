from application.infra.reader.builder import SetTearBuilder
from application.setupteardown.models import SetupTeardown


class DirConfigure(object):

    def __init__(self, module_id, module_type):
        self.module_id = module_id
        self.module_type = module_type
        self.st_builder = SetTearBuilder()

    def get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        obj = st_queryset.first()
        st_str = self.st_builder.get_from_object(obj)
        return st_str

    def get(self):
        ctx = self.get_setup_and_teardown()
        if ctx:
            return self.st_builder._setting_line + ctx
        return None
