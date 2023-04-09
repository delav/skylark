from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.region.models import Region
from application.region.serializers import RegionSerializers

# Create your views here.


class RegionViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                     mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all regions')
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
            return JsonResponse(code=10401, msg='create environment failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update region: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            self.perform_update(serializer)
        except Exception as e:
            logger.error(f'update region failed: {e}')
            return JsonResponse(code=10403, msg='update region failed')
        return JsonResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
