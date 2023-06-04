from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_dir_node, handler_suite_node

# Create your views here.


class TestSuiteViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TestSuite.objects.all()
    serializer_class = TestSuiteSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get child dir and suite by dir id: {request.query_params}')
        try:
            dir_id = request.query_params.get('dir')
            dir_obj = SuiteDir.objects.get(id=dir_id)
        except (Exception,) as e:
            logger.error(f'get dir child info failed: {e}')
            return JsonResponse(code=10060, msg='get dir child info failed')
        child_dirs = dir_obj.children.all()
        child_suites = dir_obj.suites.all()
        node_list = []
        for item in child_dirs.iterator():
            dir_data = SuiteDirSerializers(item).data
            if item.category != settings.CATEGORY_META.get('TestCase'):
                dir_data['extra_data'] = {}
            else:
                dir_data['extra_data'] = get_model_extra_data(item.id, settings.MODULE_TYPE_META.get('SuiteDir'))
            node_list.append(handler_dir_node(dir_data))
        for item in child_suites.iterator():
            suite_data = self.get_serializer(item).data
            if item.category != settings.CATEGORY_META.get('TestCase'):
                suite_data['extra_data'] = {}
            else:
                suite_data['extra_data'] = get_model_extra_data(item.id, settings.MODULE_TYPE_META.get('TestSuite'))
            node_list.append(handler_suite_node(suite_data))
        return JsonResponse(data=node_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create test suite: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except (Exception,) as e:
            logger.error(f'save test suite failed: {e}')
            return JsonResponse(code=10061, msg='create test suite failed')
        suite_data = serializer.data
        if suite_data['category'] != settings.CATEGORY_META.get('TestCase'):
            suite_data['extra_data'] = {}
        else:
            suite_data['extra_data'] = get_model_extra_data(suite_data['id'], settings.MODULE_TYPE_META.get('TestSuite'))
        result = handler_suite_node(suite_data)
        return JsonResponse(data=result)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        logger.info(f'update test suite: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except (Exception,) as e:
            logger.error(f'update test suite failed: {e}')
            return JsonResponse(code=10063, msg='update test suite failed')
        return JsonResponse(data=serializer.data)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete test suite: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete test suite error: {e}')
            return JsonResponse(code=10064, msg='delete test suite failed')
        return JsonResponse()
