

class CommonStructure(object):
    def __init__(
            self,
            init_file_paths,
            common_file_sources,
            common_variable_files,
            external_files
    ):
        self._init_paths = init_file_paths
        self._sources = common_file_sources
        self._variable_files = common_variable_files
        self._external_files = external_files

    def get_init_file_path(self):
        return self._init_paths

    def get_common_path(self):
        return self._sources.keys()

    def get_common_source(self):
        return self._sources

    def get_variable_files(self):
        return self._variable_files

    def get_external_files(self):
        return self._external_files


class SuiteStructure(object):

    def __init__(self):
        self._path = ''
        self._header = ''
        self._testcase = []
        self._text = ''

    def set_path(self, path):
        self._path = path

    def set_header(self, header):
        self._header = header

    def set_testcase(self, cases):
        self._testcase = cases

    def set_content(self, text):
        self._text = text

    def get_header(self):
        return self._header

    def get_path(self):
        return self._path

    def get_content(self):
        return self._text

    def get_case(self):
        return self._testcase

    def case_count(self):
        return len(self._testcase)


class Structure(object):

    def __init__(self,
                 total_cases=0,
                 common_structure=None,
                 suite_structures=None
                 ):
        if suite_structures is None:
            suite_structures = []
        self.total_cases = total_cases
        self.common_structure = common_structure
        self.suite_structures = suite_structures

    def increase_case(self, number):
        self.total_cases += number

    def add_suite(self, suite_structure):
        self.suite_structures.append(suite_structure)

    def set_common(self, common_structure):
        self.common_structure = common_structure
