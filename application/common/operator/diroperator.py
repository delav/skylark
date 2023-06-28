from infra.utils.timehanldler import get_partial_timestamp
from application.constant import *
from application.setupteardown.models import SetupTeardown
from application.suitedir.models import SuiteDir
from application.testsuite.models import TestSuite
from application.variable.models import Variable
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
            if dir_obj.category == ModuleCategory.TESTCASE:
                self._copy_fixture(dir_obj.id, new_dir.id)
                # not use
                # self._copy_variable(old_dir.id, new_dir.id)
            self._copy_all_suite(dir_obj, new_dir)

    def copy_dir_by_id(self, old_dir_id, new_dir_id):
        dir_obj = SuiteDir.objects.get(id=old_dir_id)
        if dir_obj.status == ModuleStatus.DELETED:
            return None
        # not allowed copy root dir
        if dir_obj.parent_dir_id is None:
            return None
        return self._copy_dir(dir_obj, new_dir_id)

    def _copy_dir(self, dir_obj, new_dir_id, new_dir_name=None):
        if not new_dir_name:
            new_dir_name = self.generate_new_name(dir_obj.name)
        new_dir = SuiteDir.objects.create(
            name=new_dir_name,
            document=dir_obj.document,
            category=dir_obj.category,
            create_by=self.create_by,
            project_id=self.new_project_id,
            parent_dir_id=new_dir_id,
            status=dir_obj.status
        )
        if dir_obj.category == ModuleCategory.TESTCASE:
            self._copy_fixture(dir_obj.id, new_dir.id)
            # not use
            # self._copy_variable(old_dir.id, new_dir.id)
        self._copy_all_suite(dir_obj, new_dir)
        child_dir_list = dir_obj.children.all()
        for child_dir in child_dir_list.iterator():
            self._copy_dir(child_dir, new_dir.id, child_dir.name)
        return new_dir

    def generate_new_name(self, old_name):
        return old_name + f'-{get_partial_timestamp(4)}copy'

    def _copy_all_suite(self, old_dir, new_dir):
        suite_query = TestSuite.objects.filter(
            suite_dir_id=old_dir.id,
            status=ModuleStatus.NORMAL
        )
        for old_suite in suite_query.iterator():
            SuiteOperator(
                self.new_project_id,
                new_dir.id,
                self.create_by,
                old_suite.name
            ).copy_suite_by_obj(old_suite)

    def _copy_fixture(self, old_dir_id, new_dir_id):
        fixture_obj = SetupTeardown.objects.get(
            module_id=old_dir_id,
            module_type=ModuleType.DIR
        )
        fixture_obj.id = None
        fixture_obj.module_id = new_dir_id
        fixture_obj.save()

    def _copy_variable(self, old_dir_id, new_dir_id):
        old_variables = Variable.objects.filter(
            module_id=old_dir_id,
            module_type=ModuleType.DIR
        )
        new_variables = []
        for variable in old_variables.iterator():
            variable.id = None
            variable.module_id = new_dir_id
            new_variables.append(variable)
        Variable.objects.bulk_create(new_variables)