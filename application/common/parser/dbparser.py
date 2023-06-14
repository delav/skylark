from infra.constant.constants import PATH_SEP, ROBOT_FILE_SUBFIX, INIT_FILE_NAME
from application.constant import *
from application.testsuite.models import TestSuite
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.reader.suitereader import DBSuiteReader
from application.common.reader.initreader import DBDirInitReader
from .baseparser import CommonParser
from .treeformat import list_to_tree, get_path_from_tree


class DBParser(CommonParser):

    def parse(self):
        common_file_paths = []
        common_file_sources = {}
        # handle variable files, will use to suite and init file
        variable_file_map = self.get_common_variable_files()
        variable_file_list = list(variable_file_map.keys())
        # handle resources, will use to suite and init file
        resources_map = self.get_common_resources(variable_file_list)
        common_file_sources.update(resources_map)
        common_file_sources.update(variable_file_map)
        resource_list = list(resources_map.keys())
        # handle case file
        case_dirs_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            status=MODULE_STATUS_META.get('Normal'),
            category=CATEGORY_META.get('TestCase')
        )
        case_dirs_ser = SuiteDirSerializers(case_dirs_queryset, many=True)
        case_dir_list = case_dirs_ser.data
        case_tree = list_to_tree(case_dir_list)
        case_path_map = get_path_from_tree(case_tree, PATH_SEP)
        for item in case_dir_list:
            # dir init file
            dir_id = item['id']
            init_path = case_path_map.get(dir_id, '')
            init_file = PATH_SEP.join([self.project_name, init_path, INIT_FILE_NAME+ROBOT_FILE_SUBFIX])
            init_text = DBDirInitReader(
                dir_id=dir_id,
                module_type=MODULE_TYPE_META.get('SuiteDir'),
                resource_list=resource_list
            ).read()
            if init_text:
                self.robot_suite.append(init_file)
                self.robot_data[init_file] = init_text
            # suite file
            suite_queryset = TestSuite.objects.filter(
                suite_dir_id=dir_id,
                status=MODULE_STATUS_META.get('Normal')
            )
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            dir_path = case_path_map.get(suite_dir_id)
            # test case
            for suite in suite_queryset.iterator():
                suite_file = PATH_SEP.join([self.project_name, dir_path, suite.name+ROBOT_FILE_SUBFIX])
                suite_reader = DBSuiteReader(
                    suite_id=suite.id,
                    module_type=MODULE_TYPE_META.get('TestSuite'),
                    suite_timeout=suite.timeout,
                    resource_list=resource_list
                )
                suite_text = suite_reader.read()
                self.total_case += suite_reader.get_suite_cases()
                self.robot_suite.append(suite_file)
                self.robot_data[suite_file] = suite_text
