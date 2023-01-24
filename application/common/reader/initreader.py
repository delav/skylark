from application.setupteardown.models import SetupTeardown
from application.variable.models import Variable
from application.infra.robot.initfile import DirInitFile


class DirInitReader(object):

    def __init__(self, dir_id, module_type, resource_list):
        self.dir_id = dir_id
        self.module_type = module_type
        self.resource_list = resource_list

    def read(self):
        return self._fetch_content()

    def _fetch_content(self):
        st_list = self._get_setup_teardown()
        if not st_list:
            return ''
        return DirInitFile(
            st_list[0],
            st_list[1],
            st_list[2],
            st_list[3],
            self._get_resource_list(),
            self._get_variable_list()
        ).get_text()

    def _get_setup_teardown(self):
        st_queryset = SetupTeardown.objects.filter(
            module_id=self.dir_id,
            module_type=self.module_type
        )
        if not st_queryset.exists():
            return None
        setup_teardown = st_queryset.first()
        return [
            setup_teardown.test_setup,
            setup_teardown.test_teardown,
            setup_teardown.suite_setup,
            setup_teardown.suite_teardown
        ]

    def _get_resource_list(self):
        return self.resource_list

    def _get_variable_list(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            module_id=self.dir_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item.name, 'value': item.value})
        return variable_list


