from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from django.conf import settings
from application.infra.django.response import JsonResponse
from application.suitedir.models import SuiteDir
from application.suitedir.serializers import SuiteDirSerializers
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.common.handler import get_model_extra_data

# Create your views here.


class SuiteDirViewSets(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin,
                       mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SuiteDir.objects.all()
    serializer_class = SuiteDirSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get project base dir by project id: {request.query_params}')
        try:
            project_id = request.query_params.get('project')
            project = Project.objects.get(id=project_id)
        except (Exception,) as e:
            logger.error(f'get base dir info failed: {e}')
            return JsonResponse(code=10070, msg='get base dir failed')
        dirs = project.dirs.filter(parent_dir=None)
        dir_list = []
        pro_data = ProjectSerializers(project).data
        for item in dirs.iterator():
            dir_data = self.get_serializer(item).data
            if item.category != settings.CATEGORY_META.get('TestCase'):
                dir_data['extra_data'] = {}
            else:
                dir_data['extra_data'] = get_model_extra_data(item.id, settings.MODULE_TYPE_META.get('SuiteDir'))
            dir_list.append(dir_data)
        data_dict = {
            'root': pro_data,
            'dirs': dir_list
        }
        return JsonResponse(data=data_dict)

    def create(self, request, *args, **kwargs):
        logger.info(f'create suite dir: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except (Exception,) as e:
            logger.error(f'save suite dir failed: {e}')
            return JsonResponse(code=10071, msg='create suite dir failed')
        result = serializer.data
        result['extra_data'] = {}
        return JsonResponse(data=result)

    def retrieve(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        logger.info(f'update suite dir: {request.data}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10072, msg='suite dir not found')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except (Exception,) as e:
            logger.error(f'update suite dir failed: {e}')
            return JsonResponse(code=10073, msg='update suite dir failed')
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete suite dir: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            if not instance.parent_dir:
                return JsonResponse(code=10074, msg='dir not allowed delete')
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete suite dir error: {e}')
            return JsonResponse(code=10075, msg='delete suite dir failed')
        return JsonResponse()
