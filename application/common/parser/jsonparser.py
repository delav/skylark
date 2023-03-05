from application.infra.constant.constants import PATH_SEP, ROBOT_FILE_SUBFIX, INIT_FILE_NAME
from application.infra.engine.structure import SuiteStructure, CommonStructure
from application.common.reader.initreader import JsonDirInitReader
from application.common.reader.suitereader import JsonSuiteReader
from application.common.parser.baseparser import BaseParser
from application.common.parser.treeformat import get_path_from_front_tree


class JsonParser(BaseParser):

    def __init__(self, project_id, project_name, env_id, run_data):
        super(JsonParser, self).__init__(
            project_id, project_name, env_id
        )
        self.run_data = run_data
        self.structures = []

    def parse(self):
        common_file_paths = []
        common_file_sources = {}
        # init variable files and resources
        self.init_sources()
        # handle project help file
        project_file_map = self.get_common_project_files()
        common_file_paths.extend(project_file_map.keys())
        common_file_sources.update(project_file_map)
        # handle variable files, will use to suite and init file
        variable_file_map = self.get_common_variable_files()
        variable_file_list = list(variable_file_map.keys())
        # handle resources, will use to suite and init file
        resources_map = self.get_common_resources()
        common_file_sources.update(resources_map)
        common_file_sources.update(variable_file_map)
        resource_list = list(resources_map.keys())
        # handle front run data
        format_data = self._parse_run_data()
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
                case_data=suite_case_data
            )
            self._extract(suite_file, suite_reader)
        common = CommonStructure(common_file_paths, common_file_sources)
        return common, self.structures

    def _parse_run_data(self):
        return get_path_from_front_tree(self.run_data, PATH_SEP)

    def _extract(self, path, reader):
        file_text = reader.read()
        struct = SuiteStructure()
        struct.set_path(path)
        struct.set_header(reader.head_text_str)
        struct.set_testcase(reader.body_text_list)
        struct.set_content(file_text)
        self.structures.append(struct)
