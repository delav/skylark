from infra.constant.constants import ENTITY_NAME_KEY, ENTITY_PARAMS_KEY, ENTITY_RETURN_KEY
from application.constant import KeywordType
from application.common.reader.module.keyword import LibKeywordManager, UserKeywordManager
from application.caseentity.models import CaseEntity


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
        ).order_by('order')
        for item in entity_queryset.iterator():
            ser_entity = {
                'keyword_id': item.keyword_id,
                'keyword_type': item.keyword_type,
                'input_args': item.input_args,
                'output_args': item.output_args
            }
            entity_list.append(self.format_entity(ser_entity))
        return entity_list


