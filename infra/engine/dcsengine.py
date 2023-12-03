

class DcsEngine(object):

    def __init__(self, **kwargs):
        self.options = kwargs
        self.batch_data = {}
        self.total_case = 0
        self.path_list = []
        self.source_map = {}
        self.variable_files = {}
        self.external_files = {}

    def visit(self, structure):
        self._init_common_data(structure.common_structure)
        suite_structures = structure.suite_structures
        for struct in suite_structures:
            self.total_case += struct.case_count()
        if self._use_multi_model(structure.total_cases):
            return self._multi_operator(suite_structures)
        self._single_operator(suite_structures)

    def _init_common_data(self, common_struct):
        init_file_paths = common_struct.get_init_file_path()
        common_sources = common_struct.get_common_source()
        self.variable_files = common_struct.get_variable_files()
        self.external_files = common_struct.get_external_files()
        self.path_list.extend(init_file_paths)
        self.source_map.update(common_sources)

    def _single_operator(self, structure_list):
        for structure in structure_list:
            path = structure.get_path()
            text = structure.get_content()
            self.path_list.append(path)
            self.source_map.update({path: text})
        self.batch_data[1] = (
            self.path_list, self.source_map, self.variable_files, self.external_files
        )

    # TODO
    def _multi_operator(self, structure_list):
        print(structure_list)
        for i in range(len(structure_list)):
            paths, sources = [], {}
            structure = structure_list[i]
            path = structure.get_path()
            text = structure.get_content()
            paths.append(path)
            sources.update({path: text})
            paths.extend(self.path_list)
            sources.update(self.source_map)
            self.batch_data[i+1] = (
                paths, sources, self.variable_files, self.external_files
            )

    def _use_multi_model(self, total_case):
        distributed_switch = self.options.get('distributed')
        max_batch_case = self.options.get('limit')
        return distributed_switch and total_case > max_batch_case

    def get_batch_data(self):
        return self.batch_data

    def get_case_count(self):
        return self.total_case
