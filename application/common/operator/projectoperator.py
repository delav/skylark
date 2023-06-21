from application.constant import ModuleType
from application.project.models import Project
from application.variable.models import Variable
from application.common.operator.diroperator import DirOperator


class ProjectOperator(object):

    def __init__(self, new_project_name, copy_project_id, **kwargs):
        self.kwargs = kwargs
        self.copy_project_id = copy_project_id
        self.name = new_project_name
        self.new_project = None

    def _create_project(self):
        project = Project.objects.create(
            name=self.name,
            **self.kwargs
        )
        self.new_project = project

    def get_new_project(self):
        return self.new_project

    def new_project_action(self):
        self._create_project()
        DirOperator(
            self.new_project.id,
            self.copy_project_id,
            self.new_project.create_by
        ).create_first_level_dir()

    def copy_project_action(self):
        self._create_project()
        self._copy_project_variable()
        DirOperator(
            self.new_project.id,
            self.copy_project_id,
            self.new_project.create_by
        ).deep_copy_all_dir()

    def _copy_project_variable(self):
        old_variable_query = Variable.objects.filter(
            module_id=self.copy_project_id,
            module_type=ModuleType.PROJECT
        )
        new_variables = []
        for variable in old_variable_query.iterator():
            variable.id = None
            variable.module_id = self.new_project.id
            new_variables.append(variable)
        Variable.objects.bulk_create(new_variables)
