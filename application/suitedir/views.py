from loguru import logger
from django.db import IntegrityError
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.constant import *
from application.manager import get_project_by_id
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.common.access.projectaccess import has_project_permission
from application.common.handler import get_model_extra_data
from application.common.ztree.generatenode import handler_dir_node
from application.common.operator.diroperator import DirDeleteOperator

# Create your views here.


class SuiteDirViewSets(mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SuiteDir.objects.all()
    serializer_class = SuiteDirSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project base dir by project id: {request.query_params}')
        project_id = request.query_params.get('project')
        if not has_project_permission(project_id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        project = get_project_by_id(project_id)
        if not project:
            return JsonResponse(code=10078, msg='project not exists')
        dirs = SuiteDir.objects.filter(
            project_id=project_id,
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
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        project = get_project_by_id(project_id)
        if not project:
            return JsonResponse(code=40078, msg='project not exist')
        parent_dir = SuiteDir.objects.filter(id=serializer.validated_data.get('parent_dir_id'))
        if not parent_dir.exists():
            return JsonResponse(code=40079, msg='parent dir not exist')
        parent_dir = parent_dir.first()
        try:
            instance = SuiteDir.objects.create(
                **serializer.validated_data,
                category=parent_dir.category,
            )
        except IntegrityError:
            return JsonResponse(code=10071, msg='dir name already exist')
        dir_data = self.get_serializer(instance).data
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
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        if instance.status != ModuleStatus.NORMAL:
            return JsonResponse(code=10074, msg='suite sir not exist')
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
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        if not instance.parent_dir:
            return JsonResponse(code=10074, msg='dir not allowed delete')
        delete_operator = DirDeleteOperator(instance.project_id, request.user.email)
        delete_operator.delete_by_obj(instance)
        return JsonResponse(data=instance.id)
