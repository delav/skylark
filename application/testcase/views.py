from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.constant import *
from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers, DuplicateTestCaseSerializers
from application.userkeyword.models import UserKeyword
from application.testsuite.models import TestSuite
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_case_node
from application.common.operator.caseoperator import CaseOperator
from infra.utils.timehanldler import get_timestamp

# Create your views here.


class TestCaseViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all test case by test suite id: {request.query_params}')
        try:
            suite_id = request.query_params.get('suite')
            suite_obj = TestSuite.objects.get(
                id=suite_id,
                status=ModuleStatus.NORMAL
            )
        except (Exception,) as e:
            logger.error(f'get test case failed: {e}')
            return JsonResponse(code=10050, msg='get test case failed')
        test_cases = suite_obj.cases.filter(status=ModuleStatus.NORMAL)
        case_list = []
        for item in test_cases.iterator():
            case_data = self.get_serializer(item).data
            if item.category != ModuleCategory.TESTCASE:
                case_data['extra_data'] = {}
            else:
                case_data['extra_data'] = get_model_extra_data(item.id, ModuleType.CASE)
            case_list.append(handler_case_node(case_data))
        return JsonResponse(data=case_list)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create test case: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            suite_id = serializer.validated_data.get('test_suite_id')
            with transaction.atomic():
                instance = TestCase.objects.create(
                    **serializer.validated_data,
                )
                if instance.category == ModuleCategory.KEYWORD:
                    suite = TestSuite.objects.select_related(
                        'suite_dir__project'
                    ).get(id=suite_id)
                    project_id = suite.suite_dir.project_id
                    UserKeyword.objects.create(
                        test_case_id=instance.id,
                        group_id=KeywordGroupType.USER,
                        project_id=project_id
                    )
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10051, msg='create test case failed')
        case_data = self.get_serializer(instance)
        if case_data['category'] != ModuleCategory.TESTCASE:
            case_data['extra_data'] = {}
        else:
            case_data['extra_data'] = get_model_extra_data(case_data['id'], ModuleType.CASE)
        result = handler_case_node(case_data)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update test case: {request.data}')
        try:
            instance = self.get_object()
            if instance.status != ModuleStatus.NORMAL:
                return JsonResponse(code=10054, data='test case not exist')
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
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
                instance.status = ModuleStatus.DELETED
                instance.name = instance.name + f'-{get_timestamp(6)}'
                instance.update_by = request.user.email
                instance.save()
                if instance.category == ModuleCategory.KEYWORD:
                    related_keyword = UserKeyword.objects.get(test_case_id=instance.id)
                    related_keyword.status = ModuleStatus.DELETED
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
        if not new_case:
            return JsonResponse(code=10056, msg='case not exist')
        case_data = self.get_serializer(new_case).data
        if case_data['category'] != ModuleCategory.TESTCASE:
            case_data['extra_data'] = {}
        else:
            case_data['extra_data'] = get_model_extra_data(case_data['id'], ModuleType.CASE)
        result = handler_case_node(case_data)
        return JsonResponse(data=result)
