from loguru import logger
from datetime import datetime, timedelta
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.manager import get_projects_by_uid
from application.status import ModuleStatus
from application.project.models import Project
from application.testcase.models import TestCase
from application.buildrecord.models import BuildRecord
from application.buildplan.models import BuildPlan
from application.buildhistory.models import BuildHistory


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
    def project_info(self, request, *args, **kwargs):
        logger.info('get statistics project data')
        project_list = get_projects_by_uid(request.user.id)
        result = []
        x_days_ago = datetime.now() - timedelta(days=30)
        for project in project_list:
            project_id = project.get('id')
            case_number = TestCase.objects.filter(
                project_id=project_id,
                status=ModuleStatus.NORMAL
            ).count()
            build_records = BuildRecord.objects.filter(
                project_id=project_id,
                create_at__gte=x_days_ago
            )
            record_list = [record.id for record in build_records]
            histories = BuildHistory.objects.filter(record_id__in=record_list)
            suc_cases, all_cases = 0, 0
            for item in histories.iterator():
                suc_cases += item.passed_case
                all_cases += item.total_case
            average = suc_cases / all_cases if all_cases != 0 else 0
            project_data = {
                'project_name': project.get('name'),
                'total_case': case_number,
                'total_build': build_records.count(),
                'average_rate': average
            }
            result.append(project_data)
        return JsonResponse(data=result)

    @action(methods=['get'], detail=False)
    def increase_info(self, request, *args, **kwargs):
        logger.info('get statistics increase data')
        recently_days = 7
        x_days_ago = datetime.now() - timedelta(days=recently_days)
        case_query_result = TestCase.objects.filter(
            status=ModuleStatus.NORMAL,
            create_at__gte=x_days_ago
        ).values('create_at__date').annotate(count=Count('id'))
        case_result = {item['create_at__date'].strftime('%Y-%m-%d'): item['count'] for item in case_query_result}
        build_query_result = BuildRecord.objects.filter(
            create_at__gte=x_days_ago
        ).values('create_at__date').annotate(count=Count('id'))
        build_result = {item['create_at__date'].strftime('%Y-%m-%d'): item['count'] for item in build_query_result}
        date_list = [datetime.now() - timedelta(days=x) for x in range(recently_days-1, -1, -1)]
        case_date_result = {date.strftime('%Y-%m-%d'): 0 for date in date_list}
        build_date_result = {date.strftime('%Y-%m-%d'): 0 for date in date_list}
        case_date_result.update(case_result)
        build_date_result.update(build_result)
        result = {
            'case_increase': case_date_result,
            'build_increase': build_date_result
        }
        return JsonResponse(data=result)
