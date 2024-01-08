from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.tag.models import Tag, ModuleTag
from application.tag.serializers import TagSerializers, ModuleTagSerializers, ModuleTagCreateSerializers
from application.manager import get_tag_list_by_project

# Create your views here.


class TagViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all tags by project: {request.query_params}')
        project_id = request.query_params.get('project')
        if not project_id or not project_id.isdigit():
            return JsonResponse(data=[])
        tag_list = get_tag_list_by_project(project_id)
        return JsonResponse(data=tag_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create tag: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update tag: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete tag: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)


class ModuleTagViewSets(mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ModuleTag.objects.all()
    serializer_class = ModuleTagSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create related module tag: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        result = {
            'id': serializer.data.get('id'),
            'tag_id': serializer.data.get('tag_id')
        }
        return JsonResponse(data=result)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete tag: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)

    @action(methods=['post'], detail=False)
    def add_tag(self, request, *args, **kwargs):
        logger.info(f'create related module tag: {request.data}')
        serializer = ModuleTagCreateSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            tag = Tag.objects.create(
                name=serializer.validated_data.get('tag_name'),
                project_id=serializer.validated_data.get('project_id')
            )
            mt = ModuleTag.objects.create(
                tag_id=tag.id,
                module_id=serializer.validated_data.get('module_id'),
                module_type=serializer.validated_data.get('module_type')
            )
            result = {
                'tag': TagSerializers(tag).data,
                'id': mt.id,
                'tag_id': mt.tag_id
            }
        return JsonResponse(data=result)
