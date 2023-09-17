from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from infra.django.pagination.paginator import PagePagination
from application.constant import ModuleStatus
from application.projectpermission.models import ProjectPermission
from application.project.models import Project
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers
from application.buildplan.models import BuildPlan
from application.buildplan.serializers import BuildPlanSerializers
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
            user_project_ids = ProjectPermission.objects.filter(
                user_id__exact=request.user.id
            ).values_list('project_id').all()
            common_project_queryset = Project.objects.filter(
                status=ModuleStatus.NORMAL,
                personal=False,
                id__in=user_project_ids
            ).values_list('id')
            personal_project_queryset = Project.objects.filter(
                status=ModuleStatus.NORMAL,
                personal=True,
                create_by=request.user.email
            ).values_list('id')
            project_ids = common_project_queryset | personal_project_queryset
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

