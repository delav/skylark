from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import Group
from .serializers import GroupSerializers
from loguru import logger


class GroupViewSets(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializers

    def list(self, request, *args, **kwargs):
        logger.info('获取所有分组成功')
        queryset = self.filter_queryset(self.get_queryset().order_by('id'))
        serializer = self.get_serializer(queryset, many=True)
        result = {'code': '0000', 'data': serializer.data}
        return Response(result)

    def get_permissions(self):
        admin_methods = ['DELETE', 'UPDATE', 'POST']
        if self.request.method in admin_methods:
            return [IsAdminUser()]
        if self.request.method == 'GET':
            return [AllowAny()]
        return [permission() for permission in self.permission_classes]
