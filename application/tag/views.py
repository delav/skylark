from loguru import logger
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.tag.models import Tag
from application.tag.serializers import TagSerializers

# Create your views here.


class TagViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                  mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all tags by project')
        project_id = request.query_params.get('project')
        queryset = self.get_queryset().filter(project_id=project_id).values('name').order_by('id')
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create tag: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            queryset = Tag.objects.filter(
                name=serializer.data['name'],
                module_id=serializer.data['module_id'],
                module_type=serializer.data['module_type']
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

    def retrieve(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
