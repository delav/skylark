from pathlib import Path
from django.conf import settings
from infra.utils.timehanldler import get_timestamp
from application.status import ModuleStatus, ModuleCategory, ModuleType, FileSaveMode
from application.suitedir.models import SuiteDir
from application.testsuite.models import TestSuite
from application.testcase.models import TestCase
from application.setupteardown.models import SetupTeardown
from application.variable.models import Variable
from application.tag.models import Tag
from application.virtualfile.models import VirtualFile
from application.virtualfile.handler import PATH_SEPARATOR, get_full_dir_path
from application.common.operator.caseoperator import CaseCopyOperator


class SuiteCopyOperator(object):

    def __init__(self, project_id, new_dir_id, create_user, suite_name=None):
        self.project_id = project_id
        self.dir_id = new_dir_id
        self.create_by = create_user
        self.suite_name = suite_name

    def copy_suite_by_id(self, suite_id):
        suite_obj = TestSuite.objects.get(id=suite_id)
        if suite_obj.status == ModuleStatus.DELETED:
            return None
        return self.copy_suite(suite_obj)

    def copy_suite_by_obj(self, suite_obj):
        return self.copy_suite(suite_obj)

    def copy_suite(self, suite_obj):
        suite_dir = SuiteDir.objects.get(id=self.dir_id)
        if suite_dir.status == ModuleStatus.DELETED:
            return None
        if suite_dir.category != suite_obj.category:
            return None
        if suite_obj.category not in [ModuleCategory.TESTCASE, ModuleCategory.KEYWORD]:
            return None
        self.generate_new_name(suite_obj.name)
        new_suite = TestSuite.objects.create(
            name=self.suite_name,
            project_id=self.project_id,
            document=suite_obj.document,
            category=suite_obj.category,
            create_by=self.create_by,
            suite_dir_id=self.dir_id,
            timeout=suite_obj.timeout,
            status=suite_obj.status
        )
        if suite_obj.category in (ModuleCategory.VARIABLE, ModuleCategory.FILE):
            self._copy_virtual_file(suite_obj, new_suite, suite_dir)
            return new_suite
        if suite_obj.category == ModuleCategory.TESTCASE:
            self._copy_fixture(suite_obj.id, new_suite.id)
            self._copy_variable(suite_obj.id, new_suite.id)
            self._copy_tag(suite_obj.id, new_suite.id)
        case_queryset = TestCase.objects.filter(
            test_suite_id=suite_obj.id,
            status=ModuleStatus.NORMAL
        )
        for old_case in case_queryset.iterator():
            CaseCopyOperator(
                self.project_id,
                new_suite.id,
                self.create_by,
                old_case.name
            ).copy_case_by_obj(old_case)
        return new_suite

    def generate_new_name(self, old_name):
        if self.suite_name is not None:
            return
        self.suite_name = old_name + f'-{get_timestamp(4)}copy'

    def _copy_fixture(self, old_suite_id, new_suite_id):
        old_fixtures = SetupTeardown.objects.filter(
            module_id=old_suite_id,
            module_type=ModuleType.SUITE
        )
        new_fixtures = []
        for fixture in old_fixtures.iterator():
            fixture.id = None
            fixture.module_id = new_suite_id
            new_fixtures.append(fixture)
        SetupTeardown.objects.bulk_create(new_fixtures)

    def _copy_variable(self, old_suite_id, new_suite_id):
        old_variables = Variable.objects.filter(
            module_id=old_suite_id,
            module_type=ModuleType.SUITE
        )
        new_variables = []
        for variable in old_variables.iterator():
            variable.id = None
            variable.module_id = new_suite_id
            new_variables.append(variable)
        Variable.objects.bulk_create(new_variables)

    def _copy_tag(self, old_suite_id, new_suite_id):
        old_tags = Tag.objects.filter(
            module_id=old_suite_id,
            module_type=ModuleType.SUITE
        )
        new_tags = []
        for tag in old_tags.iterator():
            tag.id = None
            tag.project_id = self.project_id
            tag.module_id = new_suite_id
            new_tags.append(tag)
        Tag.objects.bulk_create(new_tags)

    def _copy_virtual_file(self, old_suite, new_suite, new_suite_dir):
        file_obj = VirtualFile.objects.get(suite_id=old_suite.id)
        if file_obj.status == ModuleStatus.DELETED:
            return
        new_file_path = PATH_SEPARATOR.join(get_full_dir_path(new_suite_dir, []))
        file_obj.id = None
        file_obj.suite_id = new_suite.id
        file_obj.file_path = new_file_path
        file_obj.save()
        if file_obj.save_mode == FileSaveMode.DB:
            return
        old_file_full_path = Path(settings.PROJECT_FILES, file_obj.file_path)
        new_file_full_path = Path(settings.PROJECT_FILES, new_file_path)
        old_file = old_file_full_path / file_obj.name
        if not old_file.exists():
            return
        Path(new_file_full_path).mkdir(parents=True, exist_ok=True)
        new_file = new_file_full_path / file_obj.name
        new_file.write_text(old_file.read_text(encoding='utf-8'), encoding='utf-8')


class SuiteDeleteOperator(object):

    def __init__(self, delete_user):
        self.update_by = delete_user

    def delete_by_obj(self, suite_obj):
        suite_obj.name = suite_obj.name + f'-{get_timestamp(6)}'
        suite_obj.update_by = self.update_by
        suite_obj.save()
