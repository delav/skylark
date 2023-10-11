from loguru import logger
from datetime import datetime
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from infra.django.response import JsonResponse
from infra.django.pagination.paginator import PagePagination
from application.manager import get_all_user
from application.user.models import User
from application.user.serializers import LoginSerializer, RegisterSerializer, UserSerializer, UserAdminSerializer
from application.usergroup.models import UserGroup

# Create your views here.


class NoAuthUserViewSets(viewsets.GenericViewSet):

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
        logger.info(f'register user: {request.data}')
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            user = serializer.save()
            group_id = request.data.get('group_id')
            group = UserGroup.objects.get(id=group_id)
            user.groups.add(group)
        ser = self.get_serializer(user)
        return JsonResponse(data=ser.data)

    @action(methods=['post'], detail=False)
    def reset(self):
        logger.info('retrieve password')
        return JsonResponse()


class NormalUserViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        logger.info('get all user')
        user_list = get_all_user()
        return JsonResponse(user_list)

    def retrieve(self, request, *args, **kwargs):
        logger.info('get current user info')
        serializer = self.get_serializer(request.user)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update current user info: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
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
        logger.info(f'add user: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            data = serializer.data
            username = data.get('email').split('@')[0]
            user = User(username=username, email=data.get('email'),
                        group_id=data.get('email'), is_superuser=data.get('is_superuser'))
            user.save()
            group = UserGroup.objects.get(id=data.get('group_id'))
            user.groups.add(group)
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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete user: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(msg=instance.id)
