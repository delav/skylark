from loguru import logger
from datetime import datetime
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from application.infra.response import JsonResponse
from application.user.models import User
from application.user.serializers import LoginSerializer, RegisterSerializer, UserAdminSerializer, UserNormalSerializer
from application.group.models import Group
from application.infra.common import PagePagination

# Create your views here.


class NoAuthUserViewSets(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop('user')
        user.last_login = datetime.now()
        user.save()
        return JsonResponse(data=serializer.validated_data)

    @action(methods=['post'], detail=False)
    def reset(self):
        logger.info('retrieve password')
        return JsonResponse()


class NormalUserViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserNormalSerializer

    def retrieve(self, request, *args, **kwargs):
        logger.info('get current user info')
        serializer = self.get_serializer(request.user)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update current user info: {request.data}')
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(data=serializer.data)


class AdminUserViewSets(mixins.ListModelMixin, mixins.UpdateModelMixin,
                        mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = (PagePagination,)

    def create(self, request, *args, **kwargs):
        logger.info(f'register user: {request.data}')
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            save_id = transaction.savepoint()
            try:
                user = serializer.save()
                group_id = request.data.get('group_id')
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
            except Exception as e:
                logger.error(f'register failed: {e}')
                transaction.savepoint_rollback(save_id)
                return JsonResponse(code=10010, msg='register fail')
            else:
                transaction.savepoint_commit(save_id)
        data = self.get_serializer(user)
        return JsonResponse(data=data)

    def list(self, request, *args, **kwargs):
        logger.info('get all users')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update user info: {request.data}')
        update_data = request.data
        try:
            instance = self.get_object()
        except (Exception,) as e:
            logger.error(f'update user info error: {e}')
            return JsonResponse(code=10011, msg='user not found')
        serializer = self.get_serializer(instance, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete user: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,) as e:
            logger.error(f'delete user error: {e}')
            return JsonResponse(code=10012, msg='delete user failed')
        self.perform_destroy(instance)
        return JsonResponse(msg=instance.id)
