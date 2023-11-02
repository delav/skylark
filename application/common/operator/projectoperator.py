from infra.utils.timehanldler import get_timestamp
from application.status import ModuleType, ModuleStatus
from application.project.models import Project
from application.variable.models import Variable
from application.common.operator.diroperator import DirCopyOperator, DirDeleteOperator


class ProjectCopyOperator(object):

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
        DirCopyOperator(
            self.new_project.id,
            self.copy_project_id,
            self.new_project.create_by
        ).create_first_level_dir()

    def copy_project_action(self):
        self._create_project()
        self._copy_project_variable()
        DirCopyOperator(
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


class ProjectDeleteOperator(object):

    def __init__(self, project_id, delete_user):
        self.project_id = project_id
        self.update_by = delete_user

    def delete_project(self):
        project_queryset = Project.objects.filter(id=self.project_id)
        if not project_queryset.exists():
            return
        project = project_queryset.first()
        project.status = ModuleStatus.DELETED
        project.name = project.name + f'_{get_timestamp(6)}'
        project.update_by = self.update_by
        project.save()
        dir_operator = DirDeleteOperator(project.id, self.update_by)
        dir_operator.delete_by_project()
