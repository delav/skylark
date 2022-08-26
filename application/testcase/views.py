from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers
from application.userkeyword.models import UserKeyword
from application.testsuite.models import TestSuite
from application.common.handler import fill_node

# Create your views here.


class TestCaseViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
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
            return JsonResponse(code=10071, msg='get test case failed')
        test_cases = suite_obj.cases.all()
        case_tree_list = []
        for c in test_cases.iterator():
            case_node = fill_node(
                {'id': c.id, 'pId': suite_obj.id, 'name': c.case_name, 'desc': 'c', 'type': c.case_type}
            )
            case_tree_list.append(case_node)
        return JsonResponse(data=case_tree_list)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info("create test case")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                ins = self.perform_create(serializer)
                if ins.case_type == 1:
                    case_id = ins.id
                    suite_id = ins.test_suite_id
                    suite = TestSuite.objects.select_related('suite_dir__project').get(id=suite_id)
                    project_id = suite.suite_dir.project_id
                    UserKeyword.objects.create(test_case_id=case_id, project_id=project_id)
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10040, msg='create test case failed')
        new_case_node = fill_node(
            {'id': ins.id, 'pId': ins.test_suite_id, 'name': ins.case_name, 'desc': 'c', 'type': ins.case_type}
        )
        return JsonResponse(data=new_case_node)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    def perform_create(self, serializer):
        return serializer.save()
