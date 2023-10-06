from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from infra.django.pagination.paginator import PagePagination
from application.manager import get_projects_by_uid
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
            if not project_id.isdigit() or project_id == '0':
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
        pg_queryset = self.paginate_queryset(queryset)
        record_list = self.get_serializer(pg_queryset, many=True).data
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
            histories = BuildHistorySerializers(history_queryset, many=True).data
            record['history'] = histories
        return JsonResponse(record)

