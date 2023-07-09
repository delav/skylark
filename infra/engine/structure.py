

class CommonStructure(object):
    def __init__(self, init_file_paths, common_file_sources, common_variable_files, external_files):
        self.init_paths = init_file_paths
        self.sources = common_file_sources
        self.variable_files = common_variable_files
        self.external_files = external_files

    def get_init_file_path(self):
        return self.init_paths

    def get_common_path(self):
        return self.sources.keys()

    def get_common_source(self):
        return self.sources

    def get_variable_files(self):
        return self.variable_files

    def get_external_files(self):
        return self.external_files


class SuiteStructure(object):

    def __init__(self):
        self.path = ''
        self.header = ''
        self.testcase = []
        self.text = ''

    def set_path(self, path):
        self.path = path

    def set_header(self, header):
        self.header = header

    def set_testcase(self, cases):
        self.testcase = cases

    def set_content(self, text):
        self.text = text

    def get_header(self):
        return self.header

    def get_path(self):
        return self.path

    def get_content(self):
        return self.text

    def get_case(self):
        return self.testcase

    def case_count(self):
        return len(self.testcase)
