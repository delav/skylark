from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from django.db import transaction
from django.conf import settings
from application.infra.django.response import JsonResponse
from application.testcase.models import TestCase
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers, CaseEntityListSerializers
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword

# Create your views here.


class CaseEntityViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CaseEntity.objects.all()
    serializer_class = CaseEntitySerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get test case entities by case id: {request.query_params}')
        try:
            case_id = request.query_params.get('case')
            entity_queryset = CaseEntity.objects.filter(test_case_id=case_id).order_by('seq_number')
        except (Exception,) as e:
            logger.error(f'get entities failed: {e}')
            return JsonResponse(code=10040, msg='get entities failed')
        ser = self.get_serializer(entity_queryset, many=True)
        return JsonResponse(data=ser.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'save test case entities: {request.data}')
        serializer = CaseEntityListSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        case_id = serializer.validated_data.get('case_id')
        entity_list = serializer.validated_data.get('entity_list')

        try:
            with transaction.atomic():
                test_case = TestCase.objects.get(id=case_id)
                test_case.update_by = request.user.email
                test_case.save()
                # delete old case entities
                old_entities = test_case.entities.all()
                old_entities.delete()
                # save new case entities
                keyword_list = self.validate_keywords(case_id, entity_list)
                CaseEntity.objects.bulk_create(keyword_list)
        except Exception as e:
            logger.error(f'update case entities failed: {case_id}, {e}')
            return JsonResponse(code=10041, msg='update case entities failed')
        return JsonResponse(msg='update case entities successful')

    def validate_keywords(self, case_id, entity_list):
        result_list = []
        lib_type = settings.KEYWORD_TYPE.get('LibKeyword')
        user_type = settings.KEYWORD_TYPE.get('UserKeyword')
        for i in range(len(entity_list)):
            entity = entity_list[i]
            entity['seq_number'] = i
            entity['test_case_id'] = case_id
            keyword_id = entity['keyword_id']
            keyword_type = entity['keyword_type']
            if keyword_type == lib_type:
                lib_kw = LibKeyword.objects.get(id=keyword_id)
                # lib keyword exists
                if lib_kw.input_params is None and entity['input_args'] is not None:
                    logger.error(
                        f'[{lib_kw.ext_name}] error keyword param type: expect {lib_kw.input_params},'
                        f'but get {entity["input_args"]}'
                    )
                    raise Exception
                if lib_kw.input_params is not None and entity['input_args'] is None:
                    logger.error(
                        f'[{lib_kw.ext_name}] error keyword param type: expect {lib_kw.input_params},'
                        f'but get {entity["input_args"]}'
                    )
                    raise Exception
            elif keyword_type == user_type:
                UserKeyword.objects.get(id=keyword_id)
            else:
                logger.error(f'keyword is not exists: {keyword_id}')
                raise Exception
            result_list.append(CaseEntity(**entity))
        return result_list
