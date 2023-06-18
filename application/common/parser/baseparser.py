from infra.constant.constants import PATH_SEP, COMMON_RESOURCE_PREFIX, RESOURCE_FILE_SUFFIX
from application.constant import *
from application.testsuite.models import TestSuite
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.reader.filereader import FileReader
from application.common.reader.resourcereader import ResourceKeywordReader, ResourceCommonReader
from .treeformat import list_to_tree, get_path_from_tree


class CommonParser(object):

    def __init__(self, project_id, project_name, env_id, region_id=None):
        self.project_id = project_id
        self.project_name = project_name
        self.env_id = env_id
        self.region_id = region_id
        self._variable_file_map = {}
        self._resource_map = {}
        self._project_file_map = {}

    def init_sources(self):
        self._variable_file_map = self._get_common_variable_files()
        self._resource_map = self._get_common_resources(self._variable_file_map)
        self._project_file_map = self._get_common_project_file()

    @property
    def common_resources(self):
        return self._resource_map

    @property
    def common_variable_files(self):
        return self._variable_file_map

    @property
    def common_project_files(self):
        return self._project_file_map

    def _get_suite_map(self, iterator, path, reader, **kwargs):
        suite_map = {}
        for suite in iterator:
            if kwargs.get('suite_id'):
                kwargs['suite_id'] = suite.id
            rd = reader(**kwargs)
            file_name = suite.name
            if suite.category == ModuleCategory.KEYWORD:
                file_name = suite.name + RESOURCE_FILE_SUFFIX
            file = PATH_SEP.join([self.project_name, path, file_name])
            text = rd.read()
            suite_map[file] = text
        return suite_map

    def _recursion_suite_path(self, category, reader, **kwargs):
        result_map = {}
        dir_queryset = SuiteDir.objects.filter(
            project_id=self.project_id,
            category=category,
            status=ModuleStatus.NORMAL
        )
        dir_ser = SuiteDirSerializers(dir_queryset, many=True)
        dir_list = dir_ser.data
        path_tree = list_to_tree(dir_list)
        path_map = get_path_from_tree(path_tree, PATH_SEP)
        for item in dir_list:
            suite_queryset = TestSuite.objects.filter(
                suite_dir_id=item['id'],
                category=category,
                status=ModuleStatus.NORMAL
            )
            if not suite_queryset.exists():
                continue
            suite = suite_queryset.first()
            suite_dir_id = suite.suite_dir_id
            if suite_dir_id not in path_map:
                continue
            dir_path = path_map[suite_dir_id]
            suite_map = self._get_suite_map(suite_queryset.iterator(), dir_path, reader, **kwargs)
            result_map.update(suite_map)
        return result_map

    def _get_common_variable_resources(self):
        """
        handle common variable file. belong resource file, too
        """
        un_name = f'{self.env_id}-{self.region_id}' if self.region_id else f'{self.env_id}'
        common_name = f'{COMMON_RESOURCE_PREFIX}{un_name}{RESOURCE_FILE_SUFFIX}'
        common_file = PATH_SEP.join([self.project_name, common_name])
        common_text = ResourceCommonReader(
            env_id=self.env_id,
            region_id=self.region_id,
            project_id=self.project_id,
            module_type=ModuleType.PROJECT
        ).read()
        if not common_text:
            return {}
        return {common_file: common_text}

    def _get_common_variable_files(self):
        return self._recursion_suite_path(
            ModuleCategory.RESOURCE,
            FileReader,
            env_id=self.env_id,
            region_id=self.region_id,
            suite_id=True,
        )

    def _get_common_resources(self, common_variable_file_list):
        resource_map = {}
        common_resource_map = self._get_common_variable_resources()
        resource_map.update(common_resource_map)
        common_resource_list = list(common_resource_map.keys())
        keyword_map = self._recursion_suite_path(
            ModuleCategory.KEYWORD,
            ResourceKeywordReader,
            suite_id=True,
            module_type=ModuleType.SUITE,
            resource_list=common_resource_list,
            variable_files=common_variable_file_list
        )
        resource_map.update(keyword_map)
        return resource_map

    def _get_common_project_file(self):
        return self._recursion_suite_path(
            ModuleCategory.FILE,
            FileReader,
            env_id=self.env_id,
            region_id=self.region_id,
            suite_id=True,
        )
