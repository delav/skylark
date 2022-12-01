from loguru import logger
from django.db import transaction
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.testsuite.models import TestSuite
from application.testsuite.serializers import TestSuiteSerializers
from application.suitedir.models import SuiteDir
from application.common.handler import fill_node

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
        dir_tree_list = []
        for d in child_dirs.iterator():
            dir_node = fill_node(
                {'id': d.id, 'pid': dir_obj.project_id, 'name': d.dir_name,
                 'desc': settings.NODE_DESC.get('SUITE_DIR'), 'type': d.dir_type
                 }
            )
            dir_tree_list.append(dir_node)
        child_suites = dir_obj.suites.all()
        for s in child_suites.iterator():
            suite_node = fill_node(
                {'id': s.id, 'pid': dir_obj.project_id, 'name': s.suite_name,
                 'desc': settings.NODE_DESC.get('TEST_SUITE'), 'type': s.suite_type
                 }
            )
            dir_tree_list.append(suite_node)
        return JsonResponse(data=dir_tree_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create test suite: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except (Exception,) as e:
            logger.error(f'save test suite failed: {e}')
            return JsonResponse(code=10061, msg='create test suite failed')
        node_data = fill_node(
            {'id': serializer.data['id'], 'pid': serializer.data['suite_dir_id'], 'name': serializer.data['suite_name'],
             'desc': settings.NODE_DESC.get('TEST_SUITE'), 'type': serializer.data['suite_type']
             }
        )
        return JsonResponse(data=node_data)

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
        node_data = fill_node(
            {'id': serializer.data['id'], 'pid': serializer.data['suite_dir_id'], 'name': serializer.data['suite_name'],
             'desc': settings.NODE_DESC.get('TEST_SUITE'), 'type': serializer.data['suite_type']
             }
        )
        return JsonResponse(data=node_data)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete test suite: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10064, msg='test suite not found')
        self.perform_destroy(instance)
        return JsonResponse()
