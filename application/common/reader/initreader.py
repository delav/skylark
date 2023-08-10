from application.setupteardown.models import SetupTeardown
from application.tag.models import Tag
from application.variable.models import Variable
from application.common.reader.module.fixture import FixtureManager
from infra.robot.initfile import DirInitFile
from infra.constant.constants import VARIABLE_NAME_KEY, VARIABLE_VALUE_KEY


class JsonDirInitReader(object):

    def __init__(self, setup_teardown_data, variable_list, resource_list, variable_files, tag_list):
        self.setup_teardown_data = setup_teardown_data
        self.variable_list = variable_list
        self.resource_list = resource_list
        self.variable_files = variable_files
        self.tag_list = tag_list

    def read(self):
        setup_teardown_data = self._get_setup_teardown()
        tags = self._get_tag_list()
        if not any([setup_teardown_data, tags, self.variable_list]):
            return ''
        return DirInitFile(
            setup_teardown_data[0],
            setup_teardown_data[1],
            setup_teardown_data[2],
            setup_teardown_data[3],
            self.resource_list,
            self.variable_files,
            tags,
            self.variable_list
        ).get_text()

    def _get_tag_list(self):
        return [item.get('name') for item in self.tag_list]

    def _get_setup_teardown(self):
        fixture_list = [
            self.setup_teardown_data.get('test_setup', ''),
            self.setup_teardown_data.get('test_teardown', ''),
            self.setup_teardown_data.get('suite_setup', ''),
            self.setup_teardown_data.get('suite_teardown', '')
        ]
        fixture_manager = FixtureManager(fixture_list)
        fixture_manager.replace_fixture_names()
        return fixture_manager.get_new_fixtures()


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
        fixture_list = [
            setup_teardown.test_setup,
            setup_teardown.test_teardown,
            setup_teardown.suite_setup,
            setup_teardown.suite_teardown
        ]
        fixture_manager = FixtureManager(fixture_list)
        fixture_manager.replace_fixture_names()
        return fixture_manager.get_new_fixtures()

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
            variable_list.append({
                VARIABLE_NAME_KEY: item.name, VARIABLE_VALUE_KEY: item.value
            })
        return variable_list


