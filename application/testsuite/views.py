from loguru import logger
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
            return JsonResponse(code=10061, msg='get dir child info failed')
        child_dirs = dir_obj.children.all()
        dir_tree_list = []
        for d in child_dirs.iterator():
            dir_node = fill_node(
                {'id': d.id, 'pId': dir_obj.project_id, 'name': d.dir_name, 'desc': 'd', 'type': d.dir_type}
            )
            dir_tree_list.append(dir_node)
        child_suites = dir_obj.suites.all()
        for s in child_suites.iterator():
            suite_node = fill_node(
                {'id': s.id, 'pId': dir_obj.project_id, 'name': s.suite_name, 'desc': 's', 'type': s.suite_type}
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
            return JsonResponse(code=10070, msg='create test suite failed')
        return JsonResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
