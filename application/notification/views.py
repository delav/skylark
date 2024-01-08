from loguru import logger
from rest_framework import viewsets
from rest_framework import mixins
from infra.django.response import JsonResponse
from application.notification.models import Notification
from application.notification.serializers import NotificationSerializers
from application.common.access.projectaccess import has_project_permission


# Create your views here.

class NotificationViewSets(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create notice setting: {self.request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.get('project_id')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        instance, _ = Notification.objects.update_or_create(
            project_id=serializer.validated_data.get('project_id'),
            defaults=serializer.validated_data
        )
        data = self.get_serializer(instance).data
        return JsonResponse(data=data)

    def list(self, request, *args, **kwargs):
        logger.info("get notice by project")
        project_id = request.query_params.get('project')
        if not project_id or not project_id.isdigit():
            return JsonResponse(code=80203, msg='Param error')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        queryset = Notification.objects.filter(project_id=project_id)
        if not queryset.exists():
            return JsonResponse(data={})
        serializer = self.get_serializer(queryset.first())
        return JsonResponse(data=serializer.data)
