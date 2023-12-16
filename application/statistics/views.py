from loguru import logger
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.status import ModuleStatus
from application.project.models import Project
from application.testcase.models import TestCase
from application.buildrecord.models import BuildRecord
from application.buildplan.models import BuildPlan


class StatisticsViewSets(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def overview(self, request, *args, **kwargs):
        logger.info('get statistics overview')
        project_count = Project.objects.filter(
            status=ModuleStatus.NORMAL
        ).count()
        case_count = TestCase.objects.filter(
            status=ModuleStatus.NORMAL
        ).count()
        build_count = BuildRecord.objects.all().count()
        periodic_count = BuildPlan.objects.filter(
            status=ModuleStatus.NORMAL,
            periodic_switch=True
        ).count()
        result = {
            'project_count': project_count,
            'case_count': case_count,
            'build_count': build_count,
            'periodic_count': periodic_count
        }
        return JsonResponse(data=result)

    @action(methods=['get'], detail=False)
    def case_info(self, request, *args, **kwargs):
        logger.info('get statistics case data')
        return JsonResponse(data={})

    @action(methods=['get'], detail=False)
    def build_info(self, request, *args, **kwargs):
        logger.info('get statistics build data')
        return JsonResponse(data={})
