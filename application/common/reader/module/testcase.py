from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers
from application.common.reader.module.entity import EntityReader
from application.infra.constant.constants import FRONT_ENTITY_KEY


class CaseReader(object):

    @staticmethod
    def _get_case_from_db(queryset):
        testcase_list = []
        entity_reader = EntityReader()
        for item in queryset.iterator():
            case_info = TestCaseSerializers(item).data
            entity_list = entity_reader.get_by_case_id(item.id)
            case_info.update({'entity': entity_list})
            testcase_list.append(case_info)
        return testcase_list

    @staticmethod
    def get_by_case_data(case_data):
        testcase_list = []
        entity_reader = EntityReader()
        for item in case_data:
            extra_data = item.pop('extra_data')
            if FRONT_ENTITY_KEY in extra_data:
                entity_list = entity_reader.get_by_entity_data(extra_data[FRONT_ENTITY_KEY])
            else:
                entity_list = entity_reader.get_by_case_id(item['id'])
            item.update({'entity': entity_list})
            testcase_list.append(item)
        return testcase_list

    def get_by_suite_id(self, suite_id):
        case_queryset = TestCase.objects.filter(
            test_suite_id=suite_id
        )
        return self._get_case_from_db(case_queryset)

    def get_by_case_ids(self, case_ids):
        case_queryset = TestCase.objects.filter(
            id__in=case_ids
        )
        return self._get_case_from_db(case_queryset)

