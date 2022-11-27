from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.response import JsonResponse
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers

# Create your views here.


class VariableViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get variables by module: {request.query_params}')
        try:
            module_id = request.query_params.get('mid')
            module_type = request.query_params.get('mtp')
            variable_queryset = Variable.objects.filter(
                module_id=module_id,
                module_type=module_type)
        except (Exception,) as e:
            logger.error(f'get variables failed: {e}')
            return JsonResponse(code=10501, msg='get variables failed')
        ser = self.get_serializer(variable_queryset, many=True)
        return JsonResponse(data=ser.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create variable: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            logger.error(f'create variable failed: {e}')
            return JsonResponse(code=10502, msg='create variable failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update variable: {request.data}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10503, msg='variable not found')
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get variable: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,):
            return JsonResponse(code=10504, msg='variable not found')
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete variable: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
        except (Exception,) as e:
            logger.error(f'delete variable error: {e}')
            return JsonResponse(code=10505, msg='delete variable failed')
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)
