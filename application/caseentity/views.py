from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from django.db import transaction
from infra.django.response import JsonResponse
from application.status import ModuleStatus, KeywordType
from application.testcase.models import TestCase
from application.caseentity.models import CaseEntity
from application.caseentity.serializers import CaseEntitySerializers, CaseEntityListSerializers
from application.libkeyword.models import LibKeyword
from application.userkeyword.models import UserKeyword
from application.common.access.projectaccess import has_project_permission

# Create your views here.


class CaseEntityViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = CaseEntity.objects.all()
    serializer_class = CaseEntitySerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get test case entities by case id: {request.query_params}')
        case_id = request.query_params.get('case')
        case_query = TestCase.objects.filter(
            id=case_id,
            status=ModuleStatus.NORMAL
        )
        if not case_query.exists():
            return JsonResponse(code=10042, msg='test case not exist')
        test_case = case_query.first()
        if not has_project_permission(test_case.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        entity_queryset = CaseEntity.objects.filter(
            test_case_id=case_id
        ).order_by('order')
        ser = self.get_serializer(entity_queryset, many=True)
        return JsonResponse(data=ser.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'save test case entities: {request.data}')
        serializer = CaseEntityListSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        case_id = serializer.validated_data.get('case_id')
        entity_list = serializer.validated_data.get('entity_list')
        with transaction.atomic():
            test_case = TestCase.objects.get(id=case_id)
            if not has_project_permission(test_case.project_id, request.user):
                return JsonResponse(code=40300, msg='403_FORBIDDEN')
            if test_case.status == ModuleStatus.DELETED:
                return JsonResponse(code=10042, msg='test case not exist')
            test_case.update_by = request.user.email
            test_case.save()
            # delete old case entities
            old_entities = test_case.entities.all()
            old_entities.delete()
            # save new case entities
            new_entities = self._get_new_entities(case_id, entity_list)
            CaseEntity.objects.bulk_create(new_entities)
        return JsonResponse(msg='update case entities successful')

    def _get_new_entities(self, case_id, entity_list):
        lib_keyword_ids, user_keyword_ids = set(), set()
        entity_object_list = []
        for i in range(len(entity_list)):
            entity = entity_list[i]
            entity['order'] = i
            entity['test_case_id'] = case_id
            keyword_id = entity['keyword_id']
            keyword_type = entity['keyword_type']
            if keyword_type == KeywordType.LIB:
                lib_keyword_ids.add(keyword_id)
            elif keyword_type == KeywordType.USER:
                user_keyword_ids.add(keyword_id)
            else:
                logger.error(f'keyword error: {keyword_id}')
                raise Exception
            entity_object_list.append(CaseEntity(**entity))
        # validate keyword valid
        lib_keywords = LibKeyword.objects.filter(
            id__in=lib_keyword_ids
        )
        if lib_keywords.count() != len(lib_keyword_ids):
            logger.error(f'lib keyword exception:')
            raise Exception
        user_keywords = UserKeyword.objects.filter(
            id__in=user_keyword_ids
        )
        if user_keywords.count() != len(user_keyword_ids):
            logger.error(f'user keyword exception:')
            raise Exception
        return entity_object_list
