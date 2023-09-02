from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.tag.models import Tag
from application.tag.serializers import TagSerializers

# Create your views here.


class TagViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all tags by project: {request.query_params}')
        project_id = request.query_params.get('project')
        result_list = []
        if project_id and isinstance(project_id, str) and project_id.isdigit():
            project_id = int(project_id)
            query_sql = f'select id,name from tag where project_id={project_id} group by name'
            queryset = Tag.objects.raw(query_sql)
            for item in queryset.iterator():
                item_data = {'id': item.id, 'name': item.name}
                result_list.append(item_data)
        return JsonResponse(data=result_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create tag: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = Tag.objects.filter(
            name=serializer.validated_data.get('name'),
            module_id=serializer.validated_data.get('module_id'),
            module_type=serializer.validated_data.get('module_type')
        )
        if not queryset.exists():
            self.perform_create(serializer)
        else:
            instance = queryset.first()
            serializer = self.get_serializer(instance)
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
