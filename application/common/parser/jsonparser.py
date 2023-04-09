from application.infra.constant.constants import PATH_SEP, ROBOT_FILE_SUBFIX, INIT_FILE_NAME
from application.infra.engine.structure import SuiteStructure, CommonStructure
from application.common.reader.initreader import JsonDirInitReader
from application.common.reader.suitereader import JsonSuiteReader
from application.common.parser.baseparser import CommonParser
from application.common.parser.treeformat import get_path_from_front_tree


class JsonParser(CommonParser):

    def __init__(self, project_id, project_name, env_id, region_id, include_cases=None):
        super(JsonParser, self).__init__(
            project_id, project_name, env_id, region_id
        )
        self.build_cases = include_cases
        self.structures = []

    def parse(self, run_data, common=None):
        common_file_paths = []
        common_file_sources = {}
        # common sources
        if common is None:
            common = self.get_common_from_parse()
        # handle project help file
        project_file_map = common.get('project_files')
        common_file_paths.extend(project_file_map.keys())
        common_file_sources.update(project_file_map)
        # handle variable files, will use to suite and init file
        variable_file_map = common.get('variable_files')
        variable_file_list = list(variable_file_map.keys())
        # handle resources, will use to suite and init file
        resources_map = common.get('resources')
        common_file_sources.update(resources_map)
        common_file_sources.update(variable_file_map)
        resource_list = list(resources_map.keys())
        # handle front run data
        format_data = get_path_from_front_tree(run_data, PATH_SEP)
        for dir_id, dir_data in format_data['dirs'].items():
            dir_path = dir_data['path']
            dir_extra_data = dir_data['data']['extra_data']
            if dir_extra_data['variables'] or dir_extra_data['fixtures']:
                init_file = PATH_SEP.join([self.project_name, dir_path, INIT_FILE_NAME + ROBOT_FILE_SUBFIX])
                init_text = JsonDirInitReader(
                    setup_teardown_data=dir_extra_data['fixtures'],
                    variable_list=dir_extra_data['variables'],
                    resource_list=resource_list,
                    variable_files=variable_file_list,
                    tag_list=dir_extra_data['tags']
                ).read()
                if not init_text:
                    continue
                common_file_paths.append(init_file)
                common_file_sources[init_file] = init_text
        for suite_id, suite_data in format_data['suites'].items():
            suite_file = PATH_SEP.join([self.project_name, suite_data['path'] + ROBOT_FILE_SUBFIX])
            suite_extra_data = suite_data['data']['extra_data']
            if suite_id not in format_data['cases']:
                continue
            suite_case_data = format_data['cases'][suite_id]
            suite_reader = JsonSuiteReader(
                setup_teardown_data=suite_extra_data['fixtures'],
                suite_timeout=suite_data['data']['timeout'],
                variable_list=suite_extra_data['variables'],
                resource_list=resource_list,
                variable_files=variable_file_list,
                tag_list=suite_extra_data['tags'],
                case_data=suite_case_data,
                include_cases=self.build_cases,
            )
            self._extract(suite_file, suite_reader)
        common = CommonStructure(common_file_paths, common_file_sources)
        return common, self.structures

    def get_common_from_parse(self):
        self.init_sources()
        return {
            'variable_files': self.common_variable_files,
            'resources': self.common_resources,
            'project_files': self.common_project_files,
        }

    def _extract(self, path, reader):
        file_text = reader.read()
        if len(reader.body_text_list) == 0:
            return
        struct = SuiteStructure()
        struct.set_path(path)
        struct.set_header(reader.head_text_str)
        struct.set_testcase(reader.body_text_list)
        struct.set_content(file_text)
        self.structures.append(struct)
