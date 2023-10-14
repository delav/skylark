from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.usergroup.models import UserGroup
from application.department.models import Department
from application.keywordgroup.models import KeywordGroup
from application.keywordgroup.serializers import KeywordGroupSerializers

# Create your views here.


class KeywordGroupViewSets(mixins.ListModelMixin, mixins.UpdateModelMixin,
                           mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = KeywordGroup.objects.all()
    serializer_class = KeywordGroupSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get request user keyword group')
        user_group_query = UserGroup.objects.filter(
            group__user=request.user
        ).select_related('group')
        if not user_group_query.exists():
            return JsonResponse(code=10801, msg='Not found user group')
        user_group = user_group_query.first()
        department = Department.objects.get(id=user_group.department_id)
        queryset = KeywordGroup.objects.filter(
            user_group_id=user_group.group.id
        )
        serializer = self.get_serializer(queryset, many=True)
        result = {
            'department': department.name,
            'group': user_group.group.name,
            'keyword_groups': serializer.data
        }
        return JsonResponse(data=result)

    def create(self, request, *args, **kwargs):
        logger.info(f'create keyword group: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update keyword group: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete keyword group: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)
