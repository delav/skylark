from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.projectversion.models import ProjectVersion
from application.projectversion.serializers import ProjectVersionSerializers
from application.common.access.projectaccess import has_project_permission
from skylark.celeryapp import app

# Create your views here.


class ProjectVersionViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProjectVersion.objects.all()
    serializer_class = ProjectVersionSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project version: {request.query_params}')
        params = request.query_params
        project_id = request.query_params.get('project')
        if not project_id or not project_id.isdigit():
            return JsonResponse(code=70100, msg='Param error')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        # content maybe huge, not need can filter
        flag = params.get('filter')
        if flag and flag.isdigit() and int(flag) != 0:
            queryset = ProjectVersion.objects.filter(
                project_id=project_id).values(
                'id', 'project_id', 'create_at', 'update_at',
                'create_by',  'update_by', 'branch', 'version', 'remark'
            )
        else:
            queryset = ProjectVersion.objects.filter(project_id=project_id)
        serializers = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializers.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create project version: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.get('project_id')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        app.send_task(
            settings.VERSION_TASK,
            queue=settings.DEFAULT_QUEUE,
            args=(project_id, serializer.validated_data)
        )
        return JsonResponse(data='send task success')

