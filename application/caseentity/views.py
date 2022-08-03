# Create your views here.
from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from django.db import transaction
from application.infra.response import JsonResponse
from application.testcase.models import TestCase
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword


class CaseEntityViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CaseEntity.objects.all()
    serializer_class = CaseEntitySerializers
    
    def list(self, request, *args, **kwargs):
        logger.info('get test case entities by case id')
        params = request.query_params
        case_id = params.get('case_id')
        entity_queryset = CaseEntity.objects.filter(test_case_id=case_id).order_by('seq_number')
        result = []
        for entity in entity_queryset.iterator():
            serializer = self.get_serializer(entity)
            entity_dict = serializer.data
            del entity_dict["case"]
            if entity_dict["keyword"] is None:
                entity_dict["keyword"] = entity_dict["user_keyword"]
            del entity_dict["user_keyword"]
            result.append(entity_dict)
        return JsonResponse(data=result)

    def create(self, request, *args, **kwargs):
        logger.info('update test case entities')
        case_id = request.data.get('case_id')
        entity_list = request.data.get('entity_list')
        test_case = TestCase.objects.filter(id=case_id)
        if not test_case.exists():
            logger.error(f'case id not exit: {case_id}')
            return JsonResponse(code=4000025, msg='case not exit')

        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                # delete old case entities
                old_entities = CaseEntity.objects.filter(case_id=case_id)
                old_entities.delete()
                # save new case entities
                keyword_list = self.handler_keywords(case_id, entity_list)
                CaseEntity.objects.bulk_update(keyword_list)
                logger.info(f'update case entities successful: {case_id}')
            except Exception as e:
                logger.error(f'update case entities failed: {case_id}, {e}')
                # rollback database
                transaction.savepoint_rollback(save_id)
                logger.info("rollback database successful")
                return JsonResponse(code=4000026, msg='update case entities failed')
            else:
                transaction.savepoint_commit(save_id)
        return JsonResponse(msg='update case entities successful')

    def handler_keyword(self, case_id, entity_list):
        update_list = []
        create_list = []
        for entity in entity_list:
            if 'id' in entity:
                update_list.append(entity)
            else:
                create_list.append(entity)

    def handler_keywords(self, case_id, entity_list):
        result_list = []
        for entity in entity_list:
            entity['test_case_id'] = case_id
            keyword_id = entity.pop('keyword')
            lib_keyword_queryset = LibKeyword.objects.filter(id=keyword_id)
            # lib keyword exists
            if lib_keyword_queryset.exists():
                lib_kw = lib_keyword_queryset.first()
                if lib_kw.input_arg is None and entity['input_parm'] is not None:
                    logger.error(f'[{lib_kw.ext_name}] error keyword param type: expect {lib_kw.input_arg},'
                                 f'but get {entity["input_parm"]}')
                    raise Exception
                if lib_kw.input_arg is not None and entity['input_parm'] is None:
                    logger.error(f'[{lib_kw.ext_name}] error keyword param type: expect {lib_kw.input_arg},'
                                 f'but get {entity["input_parm"]}')
                    raise Exception
                entity['lib_keyword_id'] = keyword_id
            # lib keyword not exists, find the user keyword
            else:
                user_keyword_queryset = UserKeyword.objects.filter(id=keyword_id)
                # user keyword exists
                if user_keyword_queryset.exists():
                    entity['user_keyword_id'] = keyword_id
                # user keyword not exists, raise error
                else:
                    logger.error(f'keyword is not exists: {keyword_id}')
                    raise Exception
            serializer = self.get_serializer(data=entity)
            serializer.is_valid(raise_exception=True)
            result_list.append(serializer.validated_data)
        return result_list
