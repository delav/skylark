from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.caseentity.models import CaseEntity
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
            return JsonResponse(code=10050, msg='get test case failed')
        test_cases = suite_obj.cases.all()
        case_tree_list = []
        for c in test_cases.iterator():
            case_node = fill_node(
                {'id': c.id, 'pid': suite_obj.id, 'name': c.case_name, 'desc': 'c', 'type': c.case_type}
            )
            case_tree_list.append(case_node)
        return JsonResponse(data=case_tree_list)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create test case: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_create(serializer)
                case_id = serializer.data['id']
                suite_id = serializer.data['test_suite_id']
                if serializer.data['case_type'] == 1:
                    suite = TestSuite.objects.select_related('suite_dir__project').get(id=suite_id)
                    project_id = suite.suite_dir.project_id
                    UserKeyword.objects.create(test_case_id=case_id, project_id=project_id)
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10051, msg='create test case failed')
        new_case_node = fill_node(
            {'id': case_id, 'pid': suite_id, 'name': serializer.data['case_name'],
             'desc': 'c', 'type': serializer.data['case_type']}
        )
        return JsonResponse(data=new_case_node)

    def retrieve(self, request, *args, **kwargs):
        pass

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        logger.info(f'update test case: {request.data}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10052, msg='test case not found')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                self.perform_update(serializer)
                case_id = serializer.data['id']
                if serializer.data['case_type'] == 1:
                    UserKeyword.objects.get(test_case_id=case_id).save()
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10053, msg='create test case failed')
        new_case_node = fill_node(
            {'id': case_id, 'pid': serializer.data['test_suite_id'], 'name': serializer.data['case_name'],
             'desc': 'c', 'type': serializer.data['case_type']}
        )
        return JsonResponse(data=new_case_node)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10054, msg='test case not found')
        try:
            with transaction.atomic():
                self.perform_destroy(instance)
                CaseEntity.objects.filter(test_case_id=instance.id).delete()
                if instance.case_type == 1:
                    UserKeyword.objects.get(test_case_id=instance.id).delete()
        except (Exception,) as e:
            logger.error(f'delete test case failed: {e}')
            return JsonResponse(code=10055, msg='delete test case failed')
        return JsonResponse()

