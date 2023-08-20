from loguru import logger
from rest_framework import viewsets
from rest_framework import mixins
from infra.django.response import JsonResponse
from application.notice.models import Notice
from application.notice.serializers import NoticeSerializers


# Create your views here.

class NoticeViewSets(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Notice.objects.all()
    serializer_class = NoticeSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create notice setting: {self.request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update notice: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def list(self, request, *args, **kwargs):
        logger.info("get notice by project")
        params = self.request.query_params
        if 'project' not in params:
            return JsonResponse(code=10203, msg='project not found')
        project_id = params.get('project')
        queryset = Notice.objects.filter(project_id=project_id)
        if not queryset.exists():
            return JsonResponse(data={})
        serializer = self.get_serializer(queryset.first())
        return JsonResponse(data=serializer.data)
