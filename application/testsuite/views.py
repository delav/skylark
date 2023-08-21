from loguru import logger
from django.db import transaction, IntegrityError
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.constant import *
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers, DuplicateTestSuiteSerializers
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.virtualfile.handler import update_file
from application.common.access.projectaccess import has_project_permission
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_dir_node, handler_suite_node
from application.common.operator.suiteoperator import SuiteOperator
from infra.utils.timehanldler import get_timestamp

# Create your views here.


class TestSuiteViewSets(mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get child dir and suite by dir id: {request.query_params}')
        dir_id = request.query_params.get('dir')
        dir_queryset = SuiteDir.objects.filter(
            id=dir_id,
            status=ModuleStatus.NORMAL
        )
        if not dir_queryset.exists():
            return JsonResponse(code=10068, msg='dir not exist')
        if dir_queryset.count() > 1:
            return JsonResponse(code=10069, msg='dir data error')
        dir_obj = dir_queryset.first()
        if not has_project_permission(dir_obj.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        child_dirs = dir_obj.children.filter(status=ModuleStatus.NORMAL)
        child_suites = dir_obj.suites.filter(status=ModuleStatus.NORMAL)
        node_list = []
        for item in child_dirs.iterator():
            dir_data = SuiteDirSerializers(item).data
            if item.category != ModuleCategory.TESTCASE:
                dir_data['extra_data'] = {}
            else:
                dir_data['extra_data'] = get_model_extra_data(item.id, ModuleType.DIR)
            node_list.append(handler_dir_node(dir_data))
        for item in child_suites.iterator():
            suite_data = self.get_serializer(item).data
            if item.category != ModuleCategory.TESTCASE:
                suite_data['extra_data'] = {}
            else:
                suite_data['extra_data'] = get_model_extra_data(item.id, ModuleType.SUITE)
            node_list.append(handler_suite_node(suite_data))
        return JsonResponse(data=node_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create test suite: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.data.get('project_id')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return JsonResponse(code=10061, msg='create test suite failed')
        suite_data = serializer.data
        if suite_data['category'] != ModuleCategory.TESTCASE:
            suite_data['extra_data'] = {}
        else:
            suite_data['extra_data'] = get_model_extra_data(suite_data['id'], ModuleType.SUITE)
        result = handler_suite_node(suite_data)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update test suite: {request.data}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        if instance.status != ModuleStatus.NORMAL:
            return JsonResponse(code=10064, msg='test suite not exist')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_update(serializer)
                if instance.category in (ModuleCategory.VARIABLE, ModuleCategory.FILE):
                    update_file(instance.id, name=instance.name)
        except IntegrityError:
            return JsonResponse(code=10063, msg='suite name already exist')
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete test suite: {kwargs.get("pk")}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        with transaction.atomic():
            instance.status = ModuleStatus.DELETED
            instance.name = instance.name + f'-{get_timestamp(6)}'
            instance.update_by = request.user.email
            instance.save()
            if instance.category in (ModuleCategory.VARIABLE, ModuleCategory.FILE):
                update_file(instance.id, status=ModuleStatus.DELETED)
        return JsonResponse(instance.id)

    @action(methods=['post'], detail=False)
    def duplicate(self, request, *args, **kwargs):
        logger.info(f'copy test suite: {request.data}')
        serializer = DuplicateTestSuiteSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        to_project_id = serializer.data.get('to_project_id')
        if not has_project_permission(to_project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        to_dir_id = serializer.data.get('to_dir_id')
        copy_suite_id = serializer.data.get('raw_suite_id')
        user = request.user.email
        with transaction.atomic():
            new_suite = SuiteOperator(
                to_project_id,
                to_dir_id,
                user
            ).copy_suite_by_id(copy_suite_id)
        if not new_suite:
            return JsonResponse(code=10066, msg='suite not exist')
        suite_data = self.get_serializer(new_suite).data
        if suite_data['category'] != ModuleCategory.TESTCASE:
            suite_data['extra_data'] = {}
        else:
            suite_data['extra_data'] = get_model_extra_data(suite_data['id'], ModuleType.SUITE)
        result = handler_suite_node(suite_data)
        return JsonResponse(data=result)
