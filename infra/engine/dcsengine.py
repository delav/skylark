

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

    def _multi_operator(self, structure_list):
        distributed_by_suite = self.options.get('suite_mode')
        if distributed_by_suite:
            self._suite_multi(structure_list)

    def _suite_multi(self, structure_list):
        batch_no = 1
        suite_batch_case = 0
        paths, sources = [], {}
        for i in range(len(structure_list)):
            structure = structure_list[i]
            path = structure.get_path()
            text = structure.get_content()
            suite_case = structure.case_count()
            if self._need_batch(suite_batch_case, suite_case):
                paths.extend(self.path_list)
                sources.update(self.source_map)
                self.batch_data[batch_no] = (
                    paths, sources, self.variable_files, self.external_files
                )
                batch_no += 1
                suite_batch_case = 0
                paths, sources = [], {}
            paths.append(path)
            sources.update({path: text})
            suite_batch_case += suite_case
            if i == len(structure_list) - 1:
                paths.extend(self.path_list)
                sources.update(self.source_map)
                self.batch_data[batch_no] = (
                    paths, sources, self.variable_files, self.external_files
                )

    def _need_batch(self, batch_count, next_count):
        max_batch_case = self.options.get('limit')
        if batch_count == 0:
            return False
        if batch_count >= max_batch_case:
            return True
        if batch_count + next_count < max_batch_case:
            return False
        if max_batch_case - batch_count < batch_count + next_count - max_batch_case:
            return True
        return False

    def _use_multi_model(self, total_case):
        distributed_switch = self.options.get('distributed')
        max_batch_case = self.options.get('limit')
        return distributed_switch and total_case > max_batch_case

    def get_batch_data(self):
        return self.batch_data

    def get_case_count(self):
        return self.total_case
