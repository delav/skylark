# Create your views here.
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from application import JsonResponse
from application.user.serializers import LoginSerializer, RegisterSerializer
from application.group.models import Group
from loguru import logger
from datetime import datetime


class UserViewSets(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop('user')
        user.last_login = datetime.now()
        user.save()
        return JsonResponse(data=serializer.validated_data)

    @action(methods=['post'], detail=False)
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                user = serializer.save()
                group_id = request.data.get('group_id')
                if group_id:
                    group = Group.objects.get(id=group_id)
                    user.groups.add(group)
            except Exception as e:
                logger.error(e)
                transaction.savepoint_rollback(save_id)
                return JsonResponse(msg='注册失败', code=3000025)
            else:
                transaction.savepoint_commit(save_id)

        return JsonResponse(msg='注册成功')



