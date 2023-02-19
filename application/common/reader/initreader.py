from application.setupteardown.models import SetupTeardown
from application.tag.models import Tag
from application.variable.models import Variable
from application.infra.robot.initfile import DirInitFile


class JsonDirInitReader(object):

    def __init__(self, setup_teardown_data, variable_list, resource_list, variable_files, tag_list):
        self.setup_teardown_data = setup_teardown_data
        self.variable_list = variable_list
        self.resource_list = resource_list
        self.variable_files = variable_files
        self.tag_list = tag_list

    def read(self):
        if not any([self.setup_teardown_data, self.tag_list, self.variable_list]):
            return ''
        return DirInitFile(
            self.setup_teardown_data['test_setup'],
            self.setup_teardown_data['test_teardown'],
            self.setup_teardown_data['suite_setup'],
            self.setup_teardown_data['suite_teardown'],
            self.resource_list,
            self.variable_files,
            self._get_tag_list(),
            self.variable_list
        ).get_text()

    def _get_tag_list(self):
        return [item['name'] for item in self.tag_list]


class DBDirInitReader(object):

    def __init__(self, dir_id, module_type, resource_list, variable_files):
        self.dir_id = dir_id
        self.module_type = module_type
        self.resource_list = resource_list
        self.variable_files = variable_files

    def read(self):
        setup_teardown_data = self._get_setup_teardown()
        tags = self._get_tag_list()
        variables = self._get_variable_list()
        if not any([setup_teardown_data, tags, variables]):
            return ''
        return DirInitFile(
            setup_teardown_data[0],
            setup_teardown_data[1],
            setup_teardown_data[2],
            setup_teardown_data[3],
            self.resource_list,
            self.variable_files,
            tags,
            variables,
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

    def _get_tag_list(self):
        tag_queryset = Tag.objects.filter(
            module_id=self.dir_id,
            module_type=self.module_type
        )
        if not tag_queryset.exists():
            return None
        return [t.name for t in tag_queryset.iterator()]

    def _get_variable_list(self):
        """
        dir variable only can use in dir setup or teardown
        """
        variable_list = []
        var_queryset = Variable.objects.filter(
            module_id=self.dir_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item.name, 'value': item.value})
        return variable_list


