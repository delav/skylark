from infra.constant.constants import ENTITY_NAME_KEY, ENTITY_PARAMS_KEY, ENTITY_RETURN_KEY
from application.constant import KeywordType
from application.common.keyword.manager import LibKeywordManager, UserKeywordManager
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers


class EntityReader(object):

    @staticmethod
    def format_entity(entity):
        if entity.get('keyword_type') == KeywordType.LIB:
            keyword_manager = LibKeywordManager
        else:
            keyword_manager = UserKeywordManager
        info = keyword_manager(
            entity.get('keyword_id'),
            entity.get('input_args'),
            entity.get('output_args')
        )
        return {
            ENTITY_NAME_KEY: info.keyword_name,
            ENTITY_PARAMS_KEY: info.entity_input,
            ENTITY_RETURN_KEY: info.entity_output
        }

    def get_by_entity_data(self, entity_data):
        entity_list = []
        for item in entity_data:
            entity_list.append(self.format_entity(item))
        return entity_list

    def get_by_case_id(self, case_id):
        entity_list = []
        entity_queryset = CaseEntity.objects.filter(
            test_case_id=case_id
        ).order_by('seq_number')
        for item in entity_queryset.iterator():
            ser_entity = CaseEntitySerializers(item).data
            entity_list.append(self.format_entity(ser_entity))
        return entity_list


