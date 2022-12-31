from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.infra.settings import CATEGORY_META
from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers
from application.userkeyword.models import UserKeyword
from application.testsuite.models import TestSuite

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
        test_cases = suite_obj.cases.all().prefetch_related('tags')
        case_list = []
        for item in test_cases.iterator():
            case_data = self.get_serializer(item).data
            case_data['extra_data'] = {}
            case_list.append(case_data)
        data_dict = {
            'cases': case_list
        }
        return JsonResponse(data=data_dict)

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
                if serializer.data['category'] == CATEGORY_META.get('Resource'):
                    suite = TestSuite.objects.select_related('suite_dir__project').get(id=suite_id)
                    project_id = suite.suite_dir.project_id
                    UserKeyword.objects.create(test_case_id=case_id, project_id=project_id)
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10051, msg='create test case failed')
        result = serializer.data
        result['extra_data'] = {}
        return JsonResponse(data=serializer.data)

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
                if serializer.data['case_type'] == CATEGORY_META.get('Resource'):
                    UserKeyword.objects.get(test_case_id=case_id).save()
        except Exception as e:
            logger.error(f'create test case failed: {e}')
            return JsonResponse(code=10053, msg='create test case failed')
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete test case: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10054, msg='test case not found')
        self.perform_destroy(instance)
        return JsonResponse()

