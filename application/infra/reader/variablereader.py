from application.variable.models import Variable
from application.infra.reader.builder import VariableBuilder
from application.infra.reader.builder.basebuilder import BaseBuilder


class VariableReader(BaseBuilder):
    def __init__(self, project_name, env, module_id, module_type):
        super(VariableReader, self).__init__()
        self.module_id = module_id
        self.module_type = module_type
        self.var_builder = VariableBuilder(project_name, env)

    def get_path(self):
        return self.var_builder.get_path()

    def get_content(self):
        ctx = self._get_variables()
        if ctx:
            return self._variable_line + ctx
        return None

    def _get_variables(self):
        var_queryset = Variable.objects.filter(
            module_id=self.module_id,
            module_type=self.module_type
        )
        if not var_queryset.exists():
            return None
        var_str = self.var_builder.get_from_queryset(var_queryset)
        return var_str
