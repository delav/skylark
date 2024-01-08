from loguru import logger
from django.db import transaction
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from application.usergroup.models import Group, UserGroup
from application.usergroup.serializers import UserGroupSerializers, UserGroupAddSerializers
from infra.django.response import JsonResponse


class AdminUserGroupViewSets(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializers
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        logger.info('get all user groups')
        queryset = UserGroup.objects.all().select_related('group')
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create user group: {request.data}')
        serializer = UserGroupAddSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            group = Group.objects.create(
                name=serializer.validated_data.get('name')
            )
            user_group = UserGroup.objects.create(
                group_id=group.id,
                department_id=serializer.validated_data.get('department_id'),
                library_path=serializer.validated_data.get('library_path')
            )
            group_data = {
                'id': group.id,
                'name': group.name,
                'department_id': user_group.department_id,
                'library_path': user_group.library_path
            }
        return JsonResponse(data=group_data)


