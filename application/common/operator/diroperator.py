from application.suitedir.models import SuiteDir


class DirOperator(object):

    def __init__(self, new_project, old_project):
        self.new_project = new_project
        self.old_project = old_project

    def create_first_level_dir(self):
        first_level_dir_queryset = SuiteDir.objects.filter(
            project_id=self.old_project.id,
            parent_dir_id=None
        )
        for dir_obj in first_level_dir_queryset.iterator():
            SuiteDir.objects.create(
                project_id=self.new_project.id,
                name=dir_obj.name,
                category=dir_obj.category,
                document=dir_obj.document,
                parent_dir_id=dir_obj.parent_dir_id
            )

    def deep_copy_all_dir(self):
        pass
