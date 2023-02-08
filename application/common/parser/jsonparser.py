from application.infra.constant.constants import PATH_SEP, ROBOT_FILE_SUBFIX, INIT_FILE_NAME
from application.infra.engine.structure import SuiteStructure, CaseStructure
from application.common.reader.initreader import JsonDirInitReader
from application.common.reader.suitereader import JsonSuiteReader
from application.common.parser.baseparser import BaseParser
from application.common.parser.treeformat import get_path_from_front_tree


class JsonParser(BaseParser):

    def _parse_run_data(self):
        return get_path_from_front_tree(self.run_data, PATH_SEP)

    def parse(self):
        # handle resources first, will use to suite and init file
        resources_map = self._get_keyword_resources()
        self.robot_data.update(resources_map)
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
                    resource_list=resource_list
                ).read()
                if not init_text:
                    continue
                self.robot_suite.append(init_file)
                self.robot_data[init_file] = init_text
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
                suite_id=suite_id,
                case_data=suite_case_data
            )
            suite_text = suite_reader.read()
            self.total_case += suite_reader.get_suite_cases()
            self.robot_suite.append(suite_file)
            self.robot_data[suite_file] = suite_text

