import re
import json
from datetime import datetime
from loguru import logger
from pathlib import Path
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from infra.django.response import JsonResponse
from infra.client.redisclient import RedisClient
from application.status import SystemInfoType
from application.manager import get_user_list
from application.constant import REDIS_SYSTEM_KEY_PREFIX
from application.systemext.models import SystemExt
from application.systemext.serializers import SystemExtSerializers, FeedbackForm

# Create your views here.


class SystemExtViewSets(viewsets.GenericViewSet):
    queryset = SystemExt.objects.all()
    serializer_class = SystemExtSerializers

    @action(methods=['get'], detail=False)
    def get_system_message(self, request, *args, **kwargs):
        logger.info('get system message')
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        user_id = request.user.id
        info_type = SystemInfoType.NOTICE
        message_queryset = SystemExt.objects.filter(
            info_type=info_type,
            expire_at__gt=datetime.now()
        )
        message_list = []
        for item in message_queryset:
            redis_key = f'{REDIS_SYSTEM_KEY_PREFIX}{user_id}:{info_type}:{item.id}'
            message = conn.get(redis_key)
            if not message:
                continue
            message_list.append(json.loads(message))
        return JsonResponse(data=message_list)

    @action(methods=['post'], detail=False)
    def read_system_message(self, request, *args, **kwargs):
        logger.info('read system message')
        message_id = request.data.get('message_id')
        if not message_id:
            return JsonResponse()
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        user_id = request.user.id
        info_type = SystemInfoType.NOTICE
        redis_key = f'{REDIS_SYSTEM_KEY_PREFIX}{user_id}:{info_type}:{message_id}'
        message = conn.get(redis_key)
        if message:
            message_dict = json.loads(message)
            message_dict['read'] = True
            conn.set(redis_key, json.dumps(message_dict))
        return JsonResponse()

    @action(methods=['post'], detail=False)
    def remove_system_message(self, request, *args, **kwargs):
        logger.info('remove system message')
        message_id = request.data.get('message_id')
        if not message_id:
            return JsonResponse()
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        user_id = request.user.id
        info_type = SystemInfoType.NOTICE
        redis_key = f'{REDIS_SYSTEM_KEY_PREFIX}{user_id}:{info_type}:{message_id}'
        conn.delete([redis_key])
        return JsonResponse()

    @action(methods=['post'], detail=False)
    def user_feedback(self, request, *args, **kwargs):
        logger.info('user feedback')
        form = FeedbackForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse(code=11904, msg='feedback failed')
        files = request.FILES.getlist('file')
        user_id = request.user.id
        info_type = form.cleaned_data.get('info_type')
        extra_data = form.cleaned_data.get('extra_data')
        file_path_list = []
        for f in files:
            if f.size > settings.FILE_SIZE_LIMIT:
                continue
            file_path = Path(settings.SYSTEM_FILES, str(user_id))
            Path(file_path).mkdir(parents=True, exist_ok=True)
            file = file_path / f.name
            if file.exists():
                pattern = r'^(.+)\.(\w+)$'
                match = re.match(pattern, f.name)
                file_name = match.group(1)
                file_suffix = '.' + match.group(2)
                name = f'{file_name}(1)' + file_suffix
                file = file_path / name
            destination = open(file, 'wb+')
            for chunk in f.chunks():
                destination.write(chunk)
            destination.close()
            file_path_list.append(file.as_posix())
        extra_dict = json.loads(extra_data)
        extra_dict['file_list'] = file_path_list
        instance = SystemExt.objects.create(
            user_id=user_id,
            info_type=info_type,
            extra_data=json.dumps(extra_dict)
        )
        data = self.get_serializer(instance).data
        return JsonResponse(data=data)


class AdminSystemExtViewSets(viewsets.GenericViewSet):
    queryset = SystemExt.objects.all()
    serializer_class = SystemExtSerializers
    permission_classes = (IsAdminUser,)

    @action(methods=['post'], detail=False)
    def publish_system_message(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        expire_at = serializer.validated_data.get('expire_at')
        if expire_at <= datetime.now():
            return JsonResponse(code=11901, msg='Expired time invalid')
        info_type = serializer.validated_data.get('info_type')
        notify_json = serializer.validated_data.get('extra_data')
        instance = SystemExt.objects.create(
            **serializer.validated_data
        )
        notify_dict = json.loads(notify_json)
        message_id = instance.id
        notify_dict['id'] = message_id
        notify_dict['read'] = False
        user_list = get_user_list()
        expired_seconds = int((expire_at - datetime.now()).total_seconds())
        conn = RedisClient(settings.ROBOT_REDIS_URL).connector
        for user in user_list:
            user_id = user.get('id')
            redis_key = f'{REDIS_SYSTEM_KEY_PREFIX}{user_id}:{info_type}:{message_id}'
            conn.set(redis_key, json.dumps(notify_dict))
            conn.expire(redis_key, expired_seconds)
        data = self.get_serializer(instance).data
        return JsonResponse(data=data)
