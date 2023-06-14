from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.casepriority.models import CasePriority
from application.casepriority.serializers import CasePrioritySerializers

# Create your views here.


class CasePriorityViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                           mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CasePriority.objects.all()
    serializer_class = CasePrioritySerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all case priority')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create case priority: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            logger.error(f'create case priority failed: {e}')
            return JsonResponse(code=10130, msg='create case priority failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update case priority: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except Exception as e:
            logger.error(f'update case priority failed: {e}')
            return JsonResponse(code=10131, msg='update case priority failed')
        return JsonResponse(serializer.data)

