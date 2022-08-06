# Create your views here.
from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from django.db import transaction
from application.infra.response import JsonResponse
from application.testcase.models import TestCase
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers, CaseEntityListSerializers
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
        result = CaseEntityListSerializers(entity_queryset, many=True)
        return JsonResponse(data=result)

    def create(self, request, *args, **kwargs):
        logger.info('update test case entities')
        serializer = CaseEntityListSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        case_id = serializer.data.get('case_id')
        entity_list = serializer.data.get('entity_list')

        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                test_case = TestCase.objects.get(id=case_id)
                test_case.update_by = request.user
                test_case.save()
                # delete old case entities
                old_entities = test_case.entity.all()
                old_entities.delete()
                # save new case entities
                keyword_list = self.validate_keywords(case_id, entity_list)
                CaseEntity.objects.bulk_create(keyword_list)
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

    def validate_keywords(self, case_id, entity_list):
        result_list = []
        for entity in entity_list:
            entity['test_case_id'] = case_id
            keyword_id = entity['keyword_id']
            keyword_type = entity['keyword_type']
            if keyword_type == 1:
                lib_kw = LibKeyword.objects.get(id=keyword_id)
                # lib keyword exists
                if lib_kw.input_arg is None and entity['input_parm'] is not None:
                    logger.error(f'[{lib_kw.ext_name}] error keyword param type: expect {lib_kw.input_arg},'
                                 f'but get {entity["input_parm"]}')
                    raise Exception
                if lib_kw.input_arg is not None and entity['input_parm'] is None:
                    logger.error(f'[{lib_kw.ext_name}] error keyword param type: expect {lib_kw.input_arg},'
                                 f'but get {entity["input_parm"]}')
                    raise Exception
                entity['lib_keyword_id'] = keyword_id
            elif keyword_type == 2:
                UserKeyword.objects.get(id=keyword_id)
            else:
                logger.error(f'keyword is not exists: {keyword_id}')
                raise Exception
            result_list.append(CaseEntity(**entity))
        return result_list
