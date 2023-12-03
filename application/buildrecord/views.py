from loguru import logger
from datetime import datetime
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from infra.django.pagination.paginator import PagePagination
from application.manager import get_projects_by_uid
from application.mapping import build_status_map
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers
from application.buildhistory.models import BuildHistory
from application.buildhistory.serializers import BuildHistorySerializers
from application.common.access.projectaccess import has_project_permission

# Create your views here.


class BuildRecordViewSets(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BuildRecord.objects.all()
    serializer_class = BuildRecordSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info(f'get record by param: {request.query_params}')
        project_id = request.query_params.get('project_id')
        if project_id:
            if not project_id.isdigit():
                return JsonResponse(code=40309, msg='Param error')
            if not has_project_permission(project_id, request.user):
                return JsonResponse(code=40300, msg='403_FORBIDDEN')
            queryset = self.get_queryset().filter(
                project_id=project_id).order_by('-create_at')
        else:
            project_list = get_projects_by_uid(request.user.id)
            project_ids = [item.get('id') for item in project_list]
            queryset = self.get_queryset().filter(
                project_id__in=project_ids).order_by('-create_at')
        create_by = request.query_params.get('create_by')
        if create_by:
            queryset = queryset.filter(create_by=create_by)
        start_date = request.query_params.get('s_date')
        end_date = request.query_params.get('e_date')
        if start_date and end_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d')
                end_date = datetime.strptime(end_date, '%Y-%m-%d')
            except (Exception,):
                pass
            else:
                queryset = queryset.filter(create_at__range=(start_date, end_date))
        pg_queryset = self.paginate_queryset(queryset)
        record_list = []
        for item in pg_queryset:
            data = self.get_serializer(item).data
            data['status_desc'] = build_status_map.get(data['status'])
            record_list.append(data)
        result = {'data': record_list, 'total': queryset.count()}
        return JsonResponse(data=result)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get record detail')
        instance = self.get_object()
        record = self.get_serializer(instance).data
        record['history'] = []
        history_queryset = BuildHistory.objects.filter(
            record_id=instance.id
        )
        if history_queryset.exists():
            history_list = []
            for item in history_queryset.iterator():
                data = BuildHistorySerializers(item).data
                data['status_desc'] = build_status_map.get(data['status'])
                history_list.append(data)
            record['history'] = history_list
        return JsonResponse(record)

    @action(methods=['get'], detail=False)
    def query_status(self, request, *args, **kwargs):
        logger.info(f'get record')
        record_id = request.query_params.get('id')
        record_query = BuildRecord.objects.filter(
            id=record_id
        )
        if not record_query.exists():
            return JsonResponse(code=50101, msg='record not found')
        data = BuildRecordSerializers(record_query.first()).data
        data['status_desc'] = build_status_map.get(data['status'])
        return JsonResponse(data=data)
