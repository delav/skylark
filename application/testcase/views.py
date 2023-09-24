from loguru import logger
from django.db import transaction, IntegrityError
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.constant import *
from application.storage import update_user_keyword_storage
from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers, DuplicateTestCaseSerializers
from application.userkeyword.models import UserKeyword
from application.testsuite.models import TestSuite
from application.common.access.projectaccess import has_project_permission
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_case_node
from application.common.operator.caseoperator import CaseCopyOperator
from infra.utils.timehanldler import get_timestamp

# Create your views here.


class TestCaseViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all test case by test suite id: {request.query_params}')
        suite_id = request.query_params.get('suite')
        suite_queryset = TestSuite.objects.filter(
            id=suite_id,
        )
        if not suite_queryset.exists():
            return JsonResponse(code=40308, msg='suite not exist')
        suite_obj = suite_queryset.first()
        if suite_obj.status == ModuleStatus.DELETED:
            return JsonResponse(code=40308, msg='suite not exist')
        if not has_project_permission(suite_obj.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        test_cases = suite_obj.cases.filter(
            status=ModuleStatus.NORMAL
        ).order_by('name')
        case_list = []
        for item in test_cases.iterator():
            case_data = self.get_serializer(item).data
            if item.category != ModuleCategory.TESTCASE:
                case_data['extra_data'] = {}
            else:
                case_data['extra_data'] = get_model_extra_data(item.id, ModuleType.CASE)
            case_list.append(handler_case_node(case_data))
        return JsonResponse(data=case_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create test case: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.get('project_id')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        try:
            test_suite = TestSuite.objects.filter(id=serializer.validated_data.get('test_suite_id'))
            if not test_suite.exists():
                return JsonResponse(code=40308, msg='suite not exist')
            test_suite = test_suite.first()
            if test_suite.status == ModuleStatus.DELETED:
                return JsonResponse(code=40308, msg='suite not exist')
            if project_id != test_suite.project_id:
                return JsonResponse(code=40309, msg='create data error')
            with transaction.atomic():
                print(serializer.validated_data)
                instance = TestCase.objects.create(
                    **serializer.validated_data,
                    category=test_suite.category,
                )
                if instance.category == ModuleCategory.KEYWORD:
                    UserKeyword.objects.create(
                        test_case_id=instance.id,
                        group_id=KeywordGroupType.USER,
                        project_id=instance.project_id
                    )
                    update_user_keyword_storage(UserKeyword, instance.id)
        except IntegrityError:
            return JsonResponse(code=40301, msg='case name already exist')
        case_data = self.get_serializer(instance).data
        if case_data['category'] != ModuleCategory.TESTCASE:
            case_data['extra_data'] = {}
        else:
            case_data['extra_data'] = get_model_extra_data(case_data['id'], ModuleType.CASE)
        result = handler_case_node(case_data)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update test case: {request.data}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        if instance.status != ModuleStatus.NORMAL:
            return JsonResponse(code=10054, msg='test case not exist')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except IntegrityError:
            return JsonResponse(code=10071, msg='case name already exist')
        if instance.category == ModuleCategory.KEYWORD:
            update_user_keyword_storage(UserKeyword, instance.id)
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete test case: {kwargs.get("pk")}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        with transaction.atomic():
            instance.status = ModuleStatus.DELETED
            instance.name = instance.name + f'-{get_timestamp(6)}'
            instance.update_by = request.user.email
            instance.save()
            if instance.category == ModuleCategory.KEYWORD:
                related_keyword = UserKeyword.objects.get(test_case_id=instance.id)
                related_keyword.status = ModuleStatus.DELETED
                related_keyword.save()
        return JsonResponse(instance.id)

    @action(methods=['post'], detail=False)
    def duplicate(self, request, *args, **kwargs):
        logger.info(f'copy test case: {request.data}')
        serializer = DuplicateTestCaseSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_project_id = serializer.data.get('to_project_id')
        if not has_project_permission(to_project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        to_suite_id = serializer.data.get('to_suite_id')
        copy_case_id = serializer.data.get('raw_case_id')
        user = request.user.email
        with transaction.atomic():
            new_case = CaseCopyOperator(
                to_project_id,
                to_suite_id,
                user
            ).copy_case_by_id(copy_case_id)
        if not new_case:
            return JsonResponse(code=10056, msg='copy error')
        case_data = self.get_serializer(new_case).data
        if case_data['category'] != ModuleCategory.TESTCASE:
            case_data['extra_data'] = {}
        else:
            case_data['extra_data'] = get_model_extra_data(case_data['id'], ModuleType.CASE)
        result = handler_case_node(case_data)
        return JsonResponse(data=result)
