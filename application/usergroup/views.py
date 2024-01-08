from loguru import logger
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from application.usergroup.models import UserGroup
from application.usergroup.serializers import UserGroupSerializers
from infra.django.response import JsonResponse


class AdminUserGroupViewSets(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializers
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        logger.info('get all user groups')
        queryset = self.get_queryset().order_by('id')
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create user group: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update user group: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete user group: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)

