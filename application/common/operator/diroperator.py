from application.constant import ModuleStatus
from application.suitedir.models import SuiteDir
from application.testsuite.models import TestSuite
from application.common.operator.suiteoperator import SuiteOperator


class DirOperator(object):

    def __init__(self, new_project_id, old_project_id, create_user):
        self.new_project_id = new_project_id
        self.old_project_id = old_project_id
        self.create_by = create_user

    def create_first_level_dir(self):
        first_level_dir_queryset = SuiteDir.objects.filter(
            project_id=self.old_project_id,
            parent_dir_id=None
        )
        for dir_obj in first_level_dir_queryset.iterator():
            SuiteDir.objects.create(
                project_id=self.new_project_id,
                name=dir_obj.name,
                category=dir_obj.category,
                document=dir_obj.document,
                parent_dir_id=dir_obj.parent_dir_id
            )

    def deep_copy_all_dir(self):
        dir_queryset = SuiteDir.objects.filter(
            project_id=self.old_project_id,
            status=ModuleStatus.NORMAL
        )
        for dir_obj in dir_queryset.iterator():
            new_dir = SuiteDir.objects.create(
                name=dir_obj.name,
                category=dir_obj.category,
                document=dir_obj.document,
                project_id=self.new_project_id,
                parent_dir_id=dir_obj.parent_dir_id,
                create_by=self.create_by
            )
            self.copy_dir(dir_obj, new_dir)

    def copy_dir(self, old_dir, new_dir):
        suite_query = TestSuite.objects.filter(
            suite_dir_id=old_dir.id,
            status=ModuleStatus.NORMAL
        )
        for old_suite in suite_query.iterator():
            SuiteOperator(
                self.new_project_id,
                new_dir.id,
                self.create_by
            ).copy_suite_by_obj(old_suite)


