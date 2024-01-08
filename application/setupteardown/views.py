from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers

# Create your views here.


class SetupTeardownViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = SetupTeardown.objects.all()
    serializer_class = SetupTeardownSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create setup teardown: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, _ = SetupTeardown.objects.update_or_create(
            defaults=serializer.validated_data,
            module_id=serializer.validated_data['module_id'],
            module_type=serializer.validated_data['module_type']
        )
        data = self.get_serializer(instance).data
        return JsonResponse(data=data)

