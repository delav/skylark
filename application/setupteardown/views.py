from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.setupteardown.models import SetupTeardown
from application.setupteardown.serializers import SetupTeardownSerializers

# Create your views here.


class SetupTeardownViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                            mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = SetupTeardown.objects.all()
    serializer_class = SetupTeardownSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create setup teardown: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            logger.error(f'create setup teardown failed: {e}')
            return JsonResponse(code=10091, msg='create setup teardown failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update setup teardown: {request.data}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10092, msg='setup teardown not found')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse()

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get setup teardown: {kwargs.get("pk")}')

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete setup teardown: {kwargs.get("pk")}')
