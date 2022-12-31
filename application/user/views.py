from loguru import logger
from datetime import datetime
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from application.infra.response import JsonResponse
from application.user.models import User
from application.user.serializers import UserSerializer, RegisterSerializer, UserAdminSerializer
from application.group.models import Group
from application.infra.pagination.paginator import PagePagination

# Create your views here.


class NoAuthUserViewSets(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(methods=['post'], detail=False)
    def login(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop('user')
        user.last_login = datetime.now()
        user.save()
        return JsonResponse(data=serializer.validated_data)

    @transaction.atomic
    @action(methods=['post'], detail=False)
    def register(self, request, *args, **kwargs):
        logger.info(f'register user: {request.data}')
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                user = serializer.save()
                group_id = request.data.get('group_id')
                group = Group.objects.get(id=group_id)
                user.groups.add(group)
        except Exception as e:
            logger.error(f'register failed: {e}')
            return JsonResponse(code=10010, msg='register fail')
        ser = self.get_serializer(user)
        return JsonResponse(data=ser.data)

    @action(methods=['post'], detail=False)
    def reset(self):
        logger.info('retrieve password')
        return JsonResponse()


class NormalUserViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'add user: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                data = serializer.data
                username = data.get('email').split('@')[0]
                user = User(username=username, email=data.get('email'),
                            group_id=data.get('email'), is_superuser=data.get('is_superuser'))
                user.save()
                group = Group.objects.get(id=data.get('group_id'))
                user.groups.add(group)
        except Exception as e:
            logger.error(f'add user failed: {e}')
            return JsonResponse(code=10010, msg='add user failed')
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
