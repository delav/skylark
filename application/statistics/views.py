from loguru import logger
from datetime import datetime, timedelta
from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from infra.utils.typetransform import id_str_to_set
from application.manager import get_projects_by_uid, get_env_list, get_region_list
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

    @action(methods=['get'], detail=False)
    def record_info(self, request, *args, **kwargs):
        logger.info('get statistics record data')
        project_id = request.query_params.get('project')
        env_map = {item.get('id'): item.get('name') for item in get_env_list()}
        region_map = {item.get('id'): item.get('name') for item in get_region_list()}
        env_rate_result = dict.fromkeys(env_map.values(), 0)
        region_rate_result = dict.fromkeys(region_map.values(), 0)
        recently_days = 30
        x_days_ago = datetime.now() - timedelta(days=recently_days)
        build_records = BuildRecord.objects.filter(
            project_id=project_id,
            create_at__gte=x_days_ago
        )
        for record in build_records.iterator():
            env_list = id_str_to_set(record.envs, to_int=True)
            region_list = id_str_to_set(record.regions, to_int=True)
            for eid in env_list:
                e_name = env_map.get(eid)
                if not e_name:
                    continue
                if e_name in env_rate_result:
                    env_rate_result[e_name] += 1
            for rid in region_list:
                r_name = region_map.get(rid)
                if not r_name:
                    continue
                if r_name in region_rate_result:
                    region_rate_result[r_name] += 1
        case_query_result = TestCase.objects.filter(
            project_id=project_id,
            status=ModuleStatus.NORMAL,
            create_at__gte=x_days_ago
        ).values('create_at__date').annotate(count=Count('id'))
        case_result = {item['create_at__date'].strftime('%Y-%m-%d'): item['count'] for item in case_query_result}
        date_list = [datetime.now() - timedelta(days=x) for x in range(recently_days - 1, -1, -1)]
        case_date_result = {date.strftime('%Y-%m-%d'): 0 for date in date_list}
        case_date_result.update(case_result)
        result = {
            'env_rate': env_rate_result,
            'region_rate': region_rate_result,
            'case_rate': case_date_result,
        }
        return JsonResponse(data=result)

    @action(methods=['get'], detail=False)
    def build_info(self, request, *args, **kwargs):
        logger.info('get statistics build data')
        project_id = request.query_params.get('project')
        region_map = {item.get('id'): item.get('name') for item in get_region_list()}
        recently_days = 30
        x_days_ago = datetime.now() - timedelta(days=recently_days)
        build_records = BuildRecord.objects.filter(
            project_id=project_id,
            create_at__gte=x_days_ago
        )
        record_list = [record.id for record in build_records]
        histories = BuildHistory.objects.filter(record_id__in=record_list).order_by('create_at')
        pass_rate, duration_rate = {}, {}
        if not region_map:
            percent_list, duration_list = [], []
            for item in histories.iterator():
                percent = round(item.passed_case / item.total_case, 3) * 100
                duration = 0
                if item.end_time:
                    duration = (item.end_time - item.start_time).total_seconds()
                percent_list.append(percent)
                duration_list.append(duration)
            pass_rate['Percent'] = percent_list
            duration_rate['Duration'] = duration_list
        else:
            for item in histories.iterator():
                r_name = region_map.get(item.region_id)
                percent = round(item.passed_case / item.total_case, 3) * 100
                duration = 0
                if item.end_time:
                    duration = (item.end_time - item.start_time).total_seconds()
                if r_name in pass_rate:
                    pass_rate[r_name].append(percent)
                else:
                    pass_rate[r_name] = [percent]
                if r_name in duration_rate:
                    duration_rate[r_name].append(duration)
                else:
                    duration_rate[r_name] = [duration]
        result_dict = {
            'pass_rate': pass_rate,
            'duration_rate': duration_rate
        }
        return JsonResponse(data=result_dict)
