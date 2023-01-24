from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.handler import get_model_extra_data

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
        dir_list, suite_list = [], []
        for item in child_dirs.iterator():
            dir_data = SuiteDirSerializers(item).data
            if item.category != settings.CATEGORY_META.get('TestCase'):
                dir_data['extra_data'] = {}
            else:
                dir_data['extra_data'] = get_model_extra_data(item.id, settings.MODULE_TYPE_META.get('SuiteDir'))
            dir_list.append(dir_data)
        for item in child_suites.iterator():
            dir_data = self.get_serializer(item).data
            if item.category != settings.CATEGORY_META.get('TestCase'):
                dir_data['extra_data'] = {}
            else:
                dir_data['extra_data'] = get_model_extra_data(item.id, settings.MODULE_TYPE_META.get('TestSuite'))
            suite_list.append(dir_data)
        data_dict = {
            'dirs': dir_list,
            'suites': suite_list
        }
        return JsonResponse(data=data_dict)

    def create(self, request, *args, **kwargs):
        logger.info(f'create test suite: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except (Exception,) as e:
            logger.error(f'save test suite failed: {e}')
            return JsonResponse(code=10061, msg='create test suite failed')
        result = serializer.data
        result['extra_data'] = {}
        return JsonResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        logger.info(f'update test suite: {request.data}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10062, msg='test suite not found')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
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
        except (Exception,):
            return JsonResponse(code=10064, msg='test suite not found')
        self.perform_destroy(instance)
        return JsonResponse()
