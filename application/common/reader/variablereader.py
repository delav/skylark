from application.variable.models import Variable
from application.infra.robot.variablefile import VariableFile


class VariableReader(object):
    def __init__(self, env, project_id, module_type):
        self.env = env
        self.project_id = project_id
        self.module_type = module_type

    def read(self):
        return self._get_common_variable()

    def _get_common_variable(self):
        variable_list = []
        var_queryset = Variable.objects.filter(
            env__env_name=self.env,
            module_id=self.project_id,
            module_type=self.module_type
        )
        for item in var_queryset.iterator():
            variable_list.append({'name': item['name'], 'value': item['value']})
        return VariableFile(variable_list)