from infra.utils.timehanldler import get_partial_timestamp
from application.constant import *
from application.testcase.models import TestCase
from application.tag.models import Tag
from application.caseentity.models import CaseEntity


class CaseOperator(object):

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
        new_case_name = case_obj.name + '-copy'
        new_case = TestCase.objects.create(
            name=new_case_name,
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
        old_tags = Tag.objects.filter(
            module_id=case_obj.id,
            module_type=ModuleType.CASE
        )
        new_tags = []
        for tag in old_tags.iterator():
            tag.id = None
            tag.project_id = self.project_id
            tag.module_id = new_case.id
            new_tags.append(tag)
        Tag.objects.bulk_create(new_tags)
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
        self.case_name = old_name + f'-{get_partial_timestamp(4)}copy'
