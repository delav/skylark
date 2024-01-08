from infra.utils.timehanldler import get_timestamp
from application.status import ModuleStatus, ModuleCategory, ModuleType
from application.testsuite.models import TestSuite
from application.testcase.models import TestCase
from application.tag.models import ModuleTag
from application.userkeyword.models import UserKeyword
from application.caseentity.models import CaseEntity


class CaseCopyOperator(object):

    def __init__(self, project_id, new_suite_id, create_user, case_name=None):
        self.project_id = project_id
        self.suite_id = new_suite_id
        self.create_by = create_user
        self.case_name = case_name

    def copy_case_by_id(self, case_id):
        case_obj = TestCase.objects.get(id=case_id)
        if case_obj.status == ModuleStatus.DELETED:
            return None
        return self.copy_case(case_obj)

    def copy_case_by_obj(self, case_obj):
        return self.copy_case(case_obj)

    def copy_case(self, case_obj):
        suite = TestSuite.objects.get(id=self.suite_id)
        if suite.status == ModuleStatus.DELETED:
            return None
        if suite.category != case_obj.category:
            return None
        if case_obj.category not in [ModuleCategory.TESTCASE, ModuleCategory.KEYWORD]:
            return None
        self.generate_new_name(case_obj.name)
        new_case = TestCase.objects.create(
            name=self.case_name,
            project_id=self.project_id,
            document=case_obj.document,
            category=case_obj.category,
            create_by=self.create_by,
            priority_id=case_obj.priority_id,
            test_suite_id=self.suite_id,
            inputs=case_obj.inputs,
            outputs=case_obj.outputs,
            timeout=case_obj.timeout,
            status=case_obj.status
        )
        if case_obj.category == ModuleCategory.TESTCASE:
            self._copy_tag(case_obj.id, new_case.id)
        if case_obj.category == ModuleCategory.KEYWORD:
            self._copy_user_keyword(case_obj.id, new_case.id)
        case_entities = case_obj.entities.all()
        entity_list = []
        for t in case_entities.iterator():
            t.id = None
            t.test_case_id = new_case.id
            entity_list.append(t)
        CaseEntity.objects.bulk_create(entity_list)
        return new_case

    def generate_new_name(self, old_name):
        if self.case_name is not None:
            return
        self.case_name = old_name + f'-{get_timestamp(4)}copy'

    def _copy_tag(self, old_case_id, new_case_id):
        old_tags = ModuleTag.objects.filter(
            module_id=old_case_id,
            module_type=ModuleType.CASE
        )
        new_tags = []
        for tag in old_tags.iterator():
            tag.id = None
            tag.module_id = new_case_id
            new_tags.append(tag)
        ModuleTag.objects.bulk_create(new_tags)

    def _copy_user_keyword(self, old_case_id, new_case_id):
        related_keyword = UserKeyword.objects.get(
            test_case_id=old_case_id
        )
        UserKeyword.objects.create(
            group_id=related_keyword.group_id,
            image=related_keyword.image,
            test_case_id=new_case_id,
            project_id=self.project_id,
            status=related_keyword.status
        )
