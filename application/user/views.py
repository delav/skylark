import random
from loguru import logger
from datetime import datetime
from django.db import transaction
from django.conf import settings
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from infra.django.response import JsonResponse
from infra.django.pagination.paginator import PagePagination
from infra.client.redisclient import RedisClient
from application.constant import REDIS_USER_INFO_KEY_PREFIX
from application.manager import get_user_list
from application.user.models import User
from application.user.serializers import (
    LoginSerializer, RegisterSerializer, ResetPasswordSerializer, UserSerializer, UserAdminSerializer
)
from application.usergroup.models import UserGroup
from application.user.handler import send_email_captcha

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
            group_id = serializer.validated_data.get('group_id')
            group = UserGroup.objects.get(id=group_id)
            user.groups.add(group)
        data = self.get_serializer(user).data
        return JsonResponse(data=data)

    @action(methods=['post'], detail=False)
    def reset_confirm(self, request, *args, **kwargs):
        logger.info('reset password confirm')
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data.get('email')
        user_query = User.objects.filter(email=user_email)
        user_query.update(password=serializer.validated_data.get('password'))
        return JsonResponse()

    @action(methods=['post'], detail=False)
    def reset_precheck(self, request, *args, **kwargs):
        logger.info('reset password send email')
        user_email = request.data.get('email')
        user_query = User.objects.filter(email=user_email)
        if not user_query.exists():
            return JsonResponse(code='10001', msg='user not exist')
        captcha = random.randint(111111, 999999)
        conn = RedisClient(settings.REDIS_URL).connector
        user = user_query.first()
        redis_key = REDIS_USER_INFO_KEY_PREFIX + f'captcha:{user.id}'
        had_send = conn.get(redis_key)
        if had_send:
            return JsonResponse(code=10002, msg='please try again later')
        from_email = settings.EMAIL_HOST_USER
        suc = send_email_captcha(user.username, from_email, [user_email], captcha)
        if not suc:
            return JsonResponse(code=10003, msg='send email failed')
        conn.set(redis_key, captcha)
        conn.expire(redis_key, 60*5)
        return JsonResponse(data='success')


class NormalUserViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        logger.info('get all user')
        user_list = get_user_list()
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
            data = serializer.validated_data
            username = data.get('email').split('@')[0]
            user = User(
                username=username,
                email=data.get('email'),
                group_id=data.get('email'),
                is_superuser=data.get('is_superuser')
            )
            user.save()
            group = UserGroup.objects.get(id=data.get('group_id'))
            user.groups.add(group)
        data = self.get_serializer(user).data
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
