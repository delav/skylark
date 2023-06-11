from application.project.models import Project
from application.common.operator.diroperator import DirOperator


class ProjectOperator(object):

    def __init__(self, new_project_name, copy_project, user):
        self.create_by = user
        self.copy_project = copy_project
        self.name = new_project_name
        self.new_project = None

    def _create_project(self):
        project = Project.objects.create(
            name=self.name,
            create_by=self.create_by,
            status=self.copy_project.status,
            personal=self.copy_project.personal
        )
        self.new_project = project

    def get_new_project(self):
        return self.new_project

    def new_project_action(self):
        self._create_project()
        DirOperator(
            self.new_project,
            self.copy_project,
            self.create_by
        ).create_first_level_dir()

    def copy_project_action(self):
        self._create_project()
        DirOperator(
            self.new_project,
            self.copy_project,
            self.create_by
        ).deep_copy_all_dir()

