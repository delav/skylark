from application.constant import (
    ROBOT_PATH_SEP, VERSION_BASE_RESOURCE_KEY, VERSION_VARIABLE_FILE_KEY, VERSION_USER_KEYWORD_KEY,
    VERSION_PROJECT_FILE_KEY, EXTRA_VARIABLE_KEY,
    EXTRA_FIXTURE_KEY, ROBOT_INIT_FILE_NAME, ROBOT_SUITE_FILE_SUFFIX, EXTRA_TAG_KEY,
)
from infra.engine.structure import SuiteStructure, CommonStructure, Structure
from application.common.reader.initreader import JsonDirInitReader
from application.common.reader.suitereader import JsonSuiteReader
from application.common.parser.baseparser import CommonParser
from application.common.parser.treeformat import parse_front_data, parse_version_data


class StructureParser(CommonParser):

    def __init__(self, project_id, project_name, env_id, region_id, include_cases=None):
        super(StructureParser, self).__init__(
            project_id, project_name, env_id, region_id
        )
        self.build_cases = include_cases

    def parse(self, run_data, common=None, from_db=False):
        if common is None:
            common = self.get_common_from_parse()
        if from_db:
            build_data = parse_version_data(run_data, ROBOT_PATH_SEP)
        else:
            build_data = parse_front_data(run_data, ROBOT_PATH_SEP)
        return self._parse(build_data, common)

    def get_common_from_parse(self):
        self.init_sources()
        return {
            VERSION_BASE_RESOURCE_KEY: self.common_base_resources,
            VERSION_VARIABLE_FILE_KEY: self.common_variable_files,
            VERSION_USER_KEYWORD_KEY: self.common_user_keywords,
            VERSION_PROJECT_FILE_KEY: self.common_project_files,
        }

    @classmethod
    def _suite_structure_builder(cls, path, reader):
        file_text = reader.read()
        if len(reader.body_text_list) == 0:
            return None
        struct = SuiteStructure()
        struct.set_path(path)
        struct.set_header(reader.head_text_str)
        struct.set_testcase(reader.body_text_list)
        struct.set_content(file_text)
        return struct

    def _parse(self, format_build_data, common_data):
        structure = Structure()
        common_file_sources = {}
        # handle base common resource
        base_resource_map = common_data.get(VERSION_BASE_RESOURCE_KEY)
        common_file_sources.update(base_resource_map)
        # handle user keyword, will use to suite and init file
        user_keyword_map = common_data.get(VERSION_USER_KEYWORD_KEY, {})
        common_file_sources.update(user_keyword_map)
        # handle variable files, will not use to suite and init file, use in command
        variable_file_map = common_data.get(VERSION_VARIABLE_FILE_KEY, {})
        # variable_file_list = list(variable_file_map.keys())
        variable_file_list = []
        # handle project help file
        project_file_map = common_data.get(VERSION_PROJECT_FILE_KEY, {})
        # need download file in slaver
        user_keyword_list = list(user_keyword_map.keys())
        init_file_paths = []
        for dir_id, dir_data in format_build_data.get('dirs', {}).items():
            dir_path = dir_data['path']
            dir_extra_data = dir_data['data']['extra_data']
            if dir_extra_data.get(EXTRA_VARIABLE_KEY) or dir_extra_data.get(EXTRA_FIXTURE_KEY):
                init_file = ROBOT_PATH_SEP.join(
                    [self.project_name, dir_path, ROBOT_INIT_FILE_NAME + ROBOT_SUITE_FILE_SUFFIX]
                )
                init_text = JsonDirInitReader(
                    setup_teardown_data=dir_extra_data.get(EXTRA_FIXTURE_KEY),
                    variable_list=dir_extra_data.get(EXTRA_VARIABLE_KEY),
                    resource_list=user_keyword_list,
                    variable_files=variable_file_list,
                    tag_list=dir_extra_data.get(EXTRA_TAG_KEY, [])
                ).read()
                if not init_text:
                    continue
                init_file_paths.append(init_file)
                common_file_sources[init_file] = init_text
        for suite_id, suite_data in format_build_data.get('suites', {}).items():
            suite_file = ROBOT_PATH_SEP.join(
                [self.project_name, suite_data['path'] + ROBOT_SUITE_FILE_SUFFIX]
            )
            suite_extra_data = suite_data['data']['extra_data']
            if suite_id not in format_build_data['cases']:
                continue
            suite_case_data = format_build_data.get('cases', {})[suite_id]
            suite_reader = JsonSuiteReader(
                setup_teardown_data=suite_extra_data.get(EXTRA_FIXTURE_KEY, {}),
                suite_timeout=suite_data['data']['timeout'],
                variable_list=suite_extra_data.get(EXTRA_VARIABLE_KEY, []),
                resource_list=user_keyword_list,
                variable_files=variable_file_list,
                tag_list=suite_extra_data.get(EXTRA_TAG_KEY, []),
                case_data=suite_case_data,
                include_cases=self.build_cases,
            )
            suite_structure = self._suite_structure_builder(suite_file, suite_reader)
            if suite_structure:
                structure.add_suite(suite_structure)
                structure.increase_case(suite_structure.case_count())
        common_structure = CommonStructure(init_file_paths, common_file_sources, variable_file_map, project_file_map)
        structure.set_common(common_structure)
        return structure
