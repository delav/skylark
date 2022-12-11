from copy import deepcopy
from application.testcase.models import TestCase
from application.caseentity.models import CaseEntity


class CaseReplicator(object):

    def __init__(self, new_suite):
        self.suite = new_suite

    def copy_case_by_id(self, case_id):
        case_obj = TestCase.objects.get(id=case_id)
        return self.copy_case(case_obj)

    def copy_case_by_obj(self, case_obj):
        return self.copy_case(case_obj)

    def copy_case(self, case):
        user_keyword_case_id = None
        new_case = deepcopy(case)
        new_case.id = None
        new_case.test_suite = self.suite
        instance = new_case.save()
        if case.category == 1:
            user_keyword_case_id = instance.id
        case_entity = case.entity.all()
        entity_list = []
        for t in case_entity.iterator():
            t.id = None
            t.test_case = instance
            entity_list.append(t)
        CaseEntity.objects.bulk_create(entity_list)
        return user_keyword_case_id


