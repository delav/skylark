from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from django.core.exceptions import ValidationError
from application.infra.response import JsonResponse
from application.testcase.models import TestCase
from application.testcase.serializers import TestCaseSerializers
from application.userkeyword.models import UserKeyword
from application.testsuite.models import TestSuite

# Create your views here.


class TestCaseViewSets(mixins.ListModelMixin, mixins.UpdateModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TestCase.objects.all()
    serializer_class = TestCaseSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get all cases by suite id')
        params = request.query_params
        suite_id = params.get('suite_id')
        try:
            case_queryset = TestCase.objects.filter(test_suite_id=suite_id).order_by('case_name')
        except ValidationError:
            return JsonResponse(code=1000036, msg='request param error')
        result = self.get_serializer(case_queryset, many=True)
        return JsonResponse(data=result)

    def create(self, request, *args, **kwargs):
        logger.info("create test case")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                instance = TestCase.objects.create(**serializer.data)
                case_id = instance.id
                suite_id = instance.test_suite_id
                suite = TestSuite.objects.select_related('suite_dir__project_id').get(id=suite_id)
                project_id = suite.suite_dir.project_id
                if instance.case_type == 1:
                    UserKeyword.objects.create(case_id=case_id, project_id=project_id)
            except Exception as e:
                logger.error(f'create test case failed: {e}')
                # rollback database
                transaction.savepoint_rollback(save_id)
                return JsonResponse(code=1000040, msg='create test case failed')
            else:
                transaction.savepoint_commit(save_id)
        return JsonResponse(data=case_id)

    def update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
