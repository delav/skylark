from application.suitedir.models import SuiteDir
from application.common.operator.suiteoperator import SuiteOperator


class DirOperator(object):

    def __init__(self, new_project, old_project, user):
        self.new_project = new_project
        self.old_project = old_project
        self.create_by = user

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
        dir_queryset = SuiteDir.objects.filter(
            project_id=self.old_project.id,
        )
        for dir_obj in dir_queryset.iterator():
            new_dir = SuiteDir.objects.create(
                name=dir_obj.name,
                category=dir_obj.category,
                document=dir_obj.document,
                project_id=self.new_project.id,
                parent_dir_id=dir_obj.parent_dir_id,
                create_by=self.create_by
            )
            self.copy_dir(dir_obj, new_dir)

    def copy_dir(self, old_dir, new_dir):
        suite_query = old_dir.suites.all()
        for old_suite in suite_query.iterator():
            SuiteOperator(
                new_dir.id,
                self.create_by
            ).copy_suite_by_obj(old_suite)


