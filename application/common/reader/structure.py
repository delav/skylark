from application.infra.settings.choices import CATEGORY_META, MODULE_TYPE_META
from application.testsuite.models import TestSuite
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.reader.suitereader import SuiteReader
from application.common.reader.resourcereader import ResourceReader
from application.common.reader.initreader import DirInitReader
from application.infra.common.tree import list_to_tree, get_path_from_tree


class Structure(object):

    path_sep = '.'
    variable_file_subfix = 'txt'
    resource_file_subfix = 'resource'
    robot_file_subfix = 'robot'
    init_file_name = '__init__'

    def __init__(self, project_id, project_name, env='test'):
        self.env = env
        self.project_id = project_id
        self.project_name = project_name
        self.map = {}

    def get_text_by_path(self):
        pass

    def parser(self, reader):
        data = reader.read()
        self.map.update(data)

    def data(self):
        return self.map

    def parser_from_json(self, data):
        result = {}
        project_id = data.get('mid')
        project_name = data.get('name')
        dir_list = data.get('children')
        for item in dir_list:
            if item['meta']['extra_data']:
                pass

    def parser_from_db(self):
        result = {'resource': {}, 'suite': {}, 'init': {}}
        # handle resources first, will use to suite and init file
        resource_dir_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            category=CATEGORY_META.get('Resource')
        )
        resource_list = []
        resource_dir_ser = SuiteDirSerializers(resource_dir_queryset, many=True)
        resource_dir_list = resource_dir_ser.data
        resource_tree = list_to_tree(resource_dir_list)
        resource_path_map = get_path_from_tree(resource_tree, self.path_sep)
        for item in resource_dir_list:
            suite_queryset = TestSuite.objects.filter(suite_dir_id=item['id'])
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            if suite_dir_id not in resource_path_map:
                continue
            dir_path = resource_path_map[suite_dir_id]
            for suite in suite_queryset.iterator():
                resource_file = self.path_sep.join([self.project_name, dir_path, suite.name, self.resource_file_subfix])
                resource_text = ResourceReader(
                    env=self.env,
                    project_id=self.project_id,
                    suite_id=suite.id,
                    module_type=MODULE_TYPE_META.get('TestSuite'),
                ).read()
                result['resource'][resource_file] = resource_text
                resource_list.append(resource_file)
        # handle case file
        case_dirs_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            category=CATEGORY_META.get('TestCase')
        )
        case_dirs_ser = SuiteDirSerializers(case_dirs_queryset, many=True)
        case_dir_list = case_dirs_ser.data
        case_tree = list_to_tree(case_dir_list)
        case_path_map = get_path_from_tree(case_tree)
        run_suites = []
        for item in case_dir_list:
            # dir init file
            dir_id = item['id']
            init_path = case_path_map.get(dir_id, '')
            init_file = self.path_sep.join([self.project_name, init_path, self.init_file_name, self.robot_file_subfix])
            init_text = DirInitReader(
                dir_id=dir_id,
                module_type=MODULE_TYPE_META.get('SuiteDir'),
                resource_list=resource_list
            ).read()
            if init_text:
                run_suites.append(init_file)
                result['init'][init_file] = init_text
            # suite file
            suite_queryset = TestSuite.objects.filter(suite_dir_id=dir_id)
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            dir_path = case_path_map.get(suite_dir_id)
            # test case
            for suite in suite_queryset.iterator():
                suite_file = self.path_sep.join([self.project_name, dir_path, suite.name, self.robot_file_subfix])
                suite_text = SuiteReader(
                    project_id=self.project_id,
                    project_name=self.project_name,
                    suite_id=suite.id,
                    module_type=MODULE_TYPE_META.get('TestSuite'),
                    suite_timeout=suite.timeout,
                    resource_list=resource_list
                ).read()
                run_suites.append(suite_file)
                result['suite'][suite_file] = suite_text
        print("suites:", run_suites)
        print("result:", result)
        return result, run_suites
