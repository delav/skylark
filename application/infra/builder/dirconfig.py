from .base import BaseBuilder
from .builders import SetTearBuilder
from application.setupteardown.models import SetupTeardown


class InitDiConfig(BaseBuilder):

    def __init__(self, module_id, module_type):
        super(InitDiConfig, self).__init__()
        self.module_id = module_id
        self.module_type = module_type

    def get_setup_and_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        obj = st_queryset.first()
        st_str = SetTearBuilder().get_from_object(obj)
        return st_str

    def get(self):
        ctx = self.get_setup_and_teardown()
        if ctx:
            return self._setting_line + self.get_setup_and_teardown()
        return None
