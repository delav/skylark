from application.common.reader.builder import VariableBuilder
from application.common.reader.basereader import BaseReader


class VariableReader(BaseReader):
    def __init__(self, project_name, env, module_id, module_type):
        super(VariableReader, self).__init__()
        self.env = env
        self.project_name = project_name
        self.module_id = module_id
        self.module_type = module_type

    def read(self):
        var_builder = VariableBuilder(self.project_name, self.module_id, self.module_type, self.env)
        path = var_builder.get_path()
        text = var_builder.get_text()
        if not text:
            return {}
        text = self._variables_line + text
        return {path: text}


