from loguru import logger
from django.db import IntegrityError
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.constant import *
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.project.models import Project
from application.common.access.projectaccess import has_project_permission
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_dir_node
from infra.utils.timehanldler import get_timestamp

# Create your views here.


class SuiteDirViewSets(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SuiteDir.objects.all()
    serializer_class = SuiteDirSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project base dir by project id: {request.query_params}')
        project_id = request.query_params.get('project')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, data='403_FORBIDDEN')
        project_queryset = Project.objects.filter(id=project_id)
        if not project_queryset.exists():
            return JsonResponse(code=10078, msg='project not exists')
        if project_queryset.count() > 1:
            return JsonResponse(code=10079, msg='project data error')
        project = project_queryset.first()
        dirs = project.dirs.filter(
            parent_dir=None,
            status=ModuleStatus.NORMAL
        ).order_by('category')
        dir_list = []
        for item in dirs.iterator():
            dir_data = self.get_serializer(item).data
            if item.category != ModuleCategory.TESTCASE:
                dir_data['extra_data'] = {}
            else:
                dir_data['extra_data'] = get_model_extra_data(item.id, ModuleType.DIR)
            dir_list.append(handler_dir_node(dir_data))
        return JsonResponse(data=dir_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create suite dir: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.get('project_id')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, data='403_FORBIDDEN')
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return JsonResponse(code=10071, msg='dir name already exist')
        dir_data = serializer.data
        if dir_data['category'] != ModuleCategory.TESTCASE:
            dir_data['extra_data'] = {}
        else:
            dir_data['extra_data'] = get_model_extra_data(dir_data['id'], ModuleType.DIR)
        result = handler_dir_node(dir_data)
        return JsonResponse(data=result)

    def update(self, request, *args, **kwargs):
        logger.info(f'update suite dir: {request.data}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, data='403_FORBIDDEN')
        if instance.status != ModuleStatus.NORMAL:
            return JsonResponse(code=10074, data='suite sir not exist')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except IntegrityError:
            return JsonResponse(code=10073, msg='update dir name already exist')
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete suite dir: {kwargs.get("pk")}')
        instance = self.get_object()
        if not has_project_permission(instance.project_id, request.user):
            return JsonResponse(code=40300, data='403_FORBIDDEN')
        if not instance.parent_dir:
            return JsonResponse(code=10074, msg='dir not allowed delete')
        instance.status = ModuleStatus.DELETED
        instance.name = instance.name + f'-{get_timestamp(6)}'
        instance.update_by = request.user.email
        instance.save()
        return JsonResponse(data=instance.id)
