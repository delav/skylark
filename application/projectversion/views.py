from loguru import logger
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.projectversion.models import ProjectVersion
from application.projectversion.serializers import ProjectVersionSerializers
from skylark.celeryapp import app

# Create your views here.


class ProjectVersionViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                             mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ProjectVersion.objects.all()
    serializer_class = ProjectVersionSerializers

    def retrieve(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        logger.info(f'get project version: {request.query_params}')
        params = request.query_params
        project_id = params.get('project')
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
        project_id = serializer.data.get('project_id')
        app.send_task(
            settings.VERSION_TASK,
            queue=settings.DEFAULT_QUEUE,
            routing_key=settings.DEFAULT_ROUTING_KEY,
            args=(project_id, serializer.data)
        )
        return JsonResponse(data='send task success')

    def update(self, request, *args, **kwargs):
        pass
