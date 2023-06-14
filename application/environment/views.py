from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.environment.models import Environment
from application.environment.serializers import EnvironmentSerializers

# Create your views here.


class EnvironmentViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                          mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all environments')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create environment: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            logger.error(f'create environment failed: {e}')
            return JsonResponse(code=10201, msg='create environment failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update environment: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            logger.error(f'update environment failed: {e}')
            return JsonResponse(code=10203, msg='update environment failed')
        return JsonResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
