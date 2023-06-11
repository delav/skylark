from loguru import logger
from django.db import transaction
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from application.infra.django.response import JsonResponse
from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers, DuplicateTestCaseSerializers
from application.userkeyword.models import UserKeyword
from application.testsuite.models import TestSuite
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_case_node
from application.common.operator.caseoperator import CaseOperator

# Create your views here.


class TestCaseViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all test case by test suite id: {request.query_params}')
        try:
            suite_id = request.query_params.get('suite')
            suite_obj = TestSuite.objects.get(id=suite_id)
        except (Exception,) as e:
            logger.error(f'get test case failed: {e}')
            return JsonResponse(code=10050, msg='get test case failed')
        test_cases = suite_obj.cases.filter(status=settings.MODULE_STATUS_META.get('Normal'))
        case_list = []
        for item in test_cases.iterator():
            case_data = self.get_serializer(item).data
            if item.category != settings.CATEGORY_META.get('TestCase'):
                case_data['extra_data'] = {}
            else:
                case_data['extra_data'] = get_model_extra_data(item.id, settings.MODULE_TYPE_META.get('TestCase'))
            case_list.append(handler_case_node(case_data))
        return JsonResponse(data=case_list)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create test case: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_create(serializer)
                case_id = serializer.data.get('id')
                suite_id = serializer.validated_data.get('test_suite_id')
                if serializer.validated_data.get('category') == settings.CATEGORY_META.get('Keyword'):
                    suite = TestSuite.objects.select_related('suite_dir__project').get(id=suite_id)
                    project_id = suite.suite_dir.project_id
                    UserKeyword.objects.create(
                        test_case_id=case_id,
                        group_id=settings.CUSTOMIZE_KEYWORD_GROUP,
                        project_id=project_id
                    )
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10051, msg='create test case failed')
        case_data = serializer.data
        if case_data['category'] != settings.CATEGORY_META.get('TestCase'):
            case_data['extra_data'] = {}
        else:
            case_data['extra_data'] = get_model_extra_data(case_data['id'], settings.MODULE_TYPE_META.get('TestCase'))
        result = handler_case_node(case_data)
        return JsonResponse(data=result)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        logger.info(f'update test case: {request.data}')
        try:
            instance = self.get_object()
            if instance.status != settings.MODULE_STATUS_META.get('Normal'):
                return JsonResponse(code=10054, data='test case not exist')
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                self.perform_update(serializer)
                case_id = serializer.validated_data.get('id')
                if serializer.validated_data.get('category') == settings.CATEGORY_META.get('Keyword'):
                    UserKeyword.objects.get(test_case_id=case_id).save()
        except Exception as e:
            logger.error(f'update test case failed: {e}')
            return JsonResponse(code=10053, msg='update test case failed')
        return JsonResponse(data=serializer.data)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete test case: {kwargs.get("pk")}')
        try:
            with transaction.atomic():
                instance = self.get_object()
                instance.status = settings.MODULE_STATUS_META.get('Deleted')
                instance.save()
                if instance.category == settings.CATEGORY_META.get('Keyword'):
                    related_keyword = UserKeyword.objects.get(test_case_id=instance.id)
                    related_keyword.status = settings.MODULE_STATUS_META.get('Deleted')
                    related_keyword.save()
        except (Exception,) as e:
            logger.error(f'delete test case error: {e}')
            return JsonResponse(code=10054, msg='delete test case failed')
        return JsonResponse()

    @transaction.atomic
    @action(methods=['post'], detail=False)
    def duplicate(self, request, *args, **kwargs):
        logger.info(f'copy test case: {request.data}')
        serializer = DuplicateTestCaseSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            to_project_id = serializer.data.get('to_project_id')
            to_suite_id = serializer.data.get('to_suite_id')
            copy_case_id = serializer.data.get('raw_case_id')
            user = request.user.email
            with transaction.atomic():
                new_case = CaseOperator(
                    to_project_id,
                    to_suite_id,
                    user
                ).copy_case_by_id(copy_case_id)
        except Exception as e:
            logger.error(f'copy test case failed: {e}')
            return JsonResponse(code=10055, msg='copy test case failed')
        case_data = self.get_serializer(new_case).data
        if case_data['category'] != settings.CATEGORY_META.get('TestCase'):
            case_data['extra_data'] = {}
        else:
            case_data['extra_data'] = get_model_extra_data(case_data['id'], settings.MODULE_TYPE_META.get('TestCase'))
        result = handler_case_node(case_data)
        return JsonResponse(data=result)
