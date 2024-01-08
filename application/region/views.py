from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from infra.django.response import JsonResponse
from application.region.models import Region
from application.region.serializers import RegionSerializers

# Create your views here.


class AdminRegionViewSets(mixins.UpdateModelMixin, mixins.ListModelMixin,
                          mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializers
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        logger.info(f'get all regions')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create region: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update region: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete region: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)
