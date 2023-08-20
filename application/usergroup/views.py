from loguru import logger
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from application.usergroup.models import UserGroup
from application.usergroup.serializers import UserGroupSerializers
from infra.django.response import JsonResponse


class UserGroupViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get all user groups')
        queryset = self.get_queryset().order_by('id')
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create user group: {request.data}')

    def update(self, request, *args, **kwargs):
        logger.info(f'update user group: {request.data}')

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete user group: {kwargs.get("pk")}')

    def get_permissions(self):
        admin_methods = ['DELETE', 'UPDATE', 'POST']
        if self.request.method in admin_methods:
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]