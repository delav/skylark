from django.conf import settings
from application.testcase.models import TestCase
from application.tag.models import Tag
from application.caseentity.models import CaseEntity


class CaseOperator(object):

    def __init__(self, project_id, new_suite_id, user):
        self.project_id = project_id
        self.suite_id = new_suite_id
        self.create_by = user

    def copy_case_by_id(self, case_id):
        case_obj = TestCase.objects.get(id=case_id)
        return self.copy_case(case_obj)

    def copy_case_by_obj(self, case_obj):
        return self.copy_case(case_obj)

    def copy_case(self, case_obj):
        user_keyword_case_id = None
        new_case = TestCase.objects.create(
            name=case_obj.name,
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
        if new_case.category == 1:
            user_keyword_case_id = new_case.id
        old_tags = Tag.objects.filter(
            module_id=case_obj.id,
            module_type=settings.MODULE_TYPE_META.get('TestCase')
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
        return user_keyword_case_id


