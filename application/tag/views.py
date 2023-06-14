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
        try:
            project_id = int(project_id)
            query_sql = f'select id,name from tag where project_id={project_id} group by name'
            result_list = []
            queryset = Tag.objects.raw(query_sql)
            for item in queryset.iterator():
                item_data = {'id': item.id, 'name': item.name}
                result_list.append(item_data)
        except (Exception,) as e:
            logger.error(f'get tags failed: {e}')
            return JsonResponse(code=10121, msg='get tags failed')
        return JsonResponse(data=result_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create tag: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
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
        except Exception as e:
            logger.error(f'create tag failed: {e}')
            return JsonResponse(code=10120, msg='create tag failed')
        return JsonResponse(data=serializer.data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        logger.info(f'update tag: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            logger.error(f'update tag failed: {e}')
            return JsonResponse(code=10121, msg='update tag failed')
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete tag: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete tag error: {e}')
            return JsonResponse(code=10125, msg='delete tag failed')
        return JsonResponse(data=instance.id)
