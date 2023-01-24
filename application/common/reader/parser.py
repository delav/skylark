from django.conf import settings
from application.infra.constant.constants import PATH_SEP, VARIABLE_FILE_SUBFIX, RESOURCE_FILE_SUBFIX, \
    ROBOT_FILE_SUBFIX, INIT_FILE_NAME
from application.testsuite.models import TestSuite
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.reader.variablereader import VariableReader
from application.common.reader.suitereader import SuiteReader
from application.common.reader.resourcereader import ResourceReader
from application.common.reader.initreader import DirInitReader
from application.infra.common.tree import list_to_tree, get_path_from_tree


class BaseParser(object):

    def __init__(self, project_id, project_name, run_data, env_id):
        self.env_id = env_id
        self.run_data = run_data
        self.project_id = project_id
        self.project_name = project_name

    def _get_common_variables(self):
        variable_map = {}
        # handle common variable file, belong resource file, too
        variable_file = PATH_SEP.join([self.project_name, f'common-{self.env_id}'+VARIABLE_FILE_SUBFIX])
        variable_text = VariableReader(
            env_id=self.env_id,
            project_id=self.project_id,
            module_type=settings.MODULE_TYPE_META.get('Project')
        ).read()
        variable_map[variable_file] = variable_text
        return variable_map

    def _get_original_resource(self, dir_list, path_map, common_variable_list):
        result_map = {}
        for item in dir_list:
            suite_queryset = TestSuite.objects.filter(suite_dir_id=item['id'])
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            if suite_dir_id not in path_map:
                continue
            dir_path = path_map[suite_dir_id]
            for suite in suite_queryset.iterator():
                resource_file = PATH_SEP.join([self.project_name, dir_path, suite.name+RESOURCE_FILE_SUBFIX])
                resource_text = ResourceReader(
                    project_id=self.project_id,
                    suite_id=suite.id,
                    module_type=settings.MODULE_TYPE_META.get('TestSuite'),
                    resource_list=common_variable_list,
                    combine=False
                ).read()
                result_map[resource_file] = resource_text
        return result_map

    def _get_combine_resource(self, dir_list, path_map, variable_list):
        resource_file = PATH_SEP.join([self.project_name, 'common-resource' + RESOURCE_FILE_SUBFIX])
        suite_id_list = []
        for item in dir_list:
            suite_queryset = TestSuite.objects.filter(suite_dir_id=item['id'])
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            if suite_dir_id not in path_map:
                continue
            for suite in suite_queryset.iterator():
                suite_id_list.append(suite.id)
        resource_text = ResourceReader(
            project_id=self.project_id,
            suite_id=suite_id_list,
            module_type=settings.MODULE_TYPE_META.get('TestSuite'),
            resource_list=variable_list,
            combine=True
        ).read()
        return {resource_file: resource_text}

    def _get_keyword_resources(self, combine=False):
        resource_map = {}
        variable_map = self._get_common_variables()
        resource_map.update(variable_map)
        common_variable_list = list(variable_map.keys())
        resource_dir_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            category=settings.CATEGORY_META.get('Resource')
        )
        resource_dir_ser = SuiteDirSerializers(resource_dir_queryset, many=True)
        resource_dir_list = resource_dir_ser.data
        resource_tree = list_to_tree(resource_dir_list)
        resource_path_map = get_path_from_tree(resource_tree, PATH_SEP)
        # resource file combine
        if combine:
            keyword_resource = self._get_combine_resource(
                resource_dir_list,
                resource_path_map,
                common_variable_list
            )
        else:
            keyword_resource = self._get_original_resource(
                resource_dir_list,
                resource_path_map,
                common_variable_list
            )
        resource_map.update(keyword_resource)
        return resource_map

    def parse_run_data(self):
        pass


class JsonParser(BaseParser):

    def parser(self):
        return {}, []


class DBParser(BaseParser):

    def parser(self):
        result = {}
        # handle resources first, will use to suite and init file
        resources_map = self._get_keyword_resources()
        result.update(resources_map)
        resource_list = list(resources_map.keys())
        # handle case file
        case_dirs_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            category=settings.CATEGORY_META.get('TestCase')
        )
        case_dirs_ser = SuiteDirSerializers(case_dirs_queryset, many=True)
        case_dir_list = case_dirs_ser.data
        case_tree = list_to_tree(case_dir_list)
        case_path_map = get_path_from_tree(case_tree, PATH_SEP)
        run_suites = []
        for item in case_dir_list:
            # dir init file
            dir_id = item['id']
            init_path = case_path_map.get(dir_id, '')
            init_file = PATH_SEP.join([self.project_name, init_path, INIT_FILE_NAME+ROBOT_FILE_SUBFIX])
            init_text = DirInitReader(
                dir_id=dir_id,
                module_type=settings.MODULE_TYPE_META.get('SuiteDir'),
                resource_list=resource_list
            ).read()
            if init_text:
                run_suites.append(init_file)
                result[init_file] = init_text
            # suite file
            suite_queryset = TestSuite.objects.filter(suite_dir_id=dir_id)
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            dir_path = case_path_map.get(suite_dir_id)
            # test case
            for suite in suite_queryset.iterator():
                suite_file = PATH_SEP.join([self.project_name, dir_path, suite.name+ROBOT_FILE_SUBFIX])
                suite_text = SuiteReader(
                    project_id=self.project_id,
                    project_name=self.project_name,
                    suite_id=suite.id,
                    module_type=settings.MODULE_TYPE_META.get('TestSuite'),
                    suite_timeout=suite.timeout,
                    resource_list=resource_list
                ).read()
                run_suites.append(suite_file)
                result[suite_file] = suite_text
        return result, run_suites
