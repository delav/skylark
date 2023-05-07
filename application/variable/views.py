from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers, BatchVariableSerializers

# Create your views here.


class VariableViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get variables by module: {request.query_params}')
        try:
            params = request.query_params
            filter_params = {
                'module_id': params.get('mid'),
                'module_type': params.get('mtp')
            }
            if params.get('env'):
                filter_params['env_id'] = params.get('env')
            if params.get('region'):
                filter_params['region_id'] = params.get('region')
            variable_queryset = Variable.objects.filter(
                **filter_params
            ).order_by('name')
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
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except (Exception,):
            return JsonResponse(code=10503, msg='update variable failed')
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
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete variable error: {e}')
            return JsonResponse(code=10505, msg='delete variable failed')
        return JsonResponse(data=instance.id)


class BatchVariableViewSets(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Variable.objects.all()
    serializer_class = BatchVariableSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'batch create variable: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            batch_list = []
            env_id = serializer.data.get('env_id')
            region_id = serializer.data.get('region_id')
            variable_list = serializer.data.get('variable_list')
            for item in variable_list:
                del item['id']
                del item['edit']
                item['env_id'] = env_id or item['env_id']
                item['region_id'] = region_id or item['region_id']
                new_obj = Variable(**item)
                batch_list.append(new_obj)
            Variable.objects.bulk_create(batch_list)
        except Exception as e:
            logger.error(f'batch create variable failed: {e}')
            return JsonResponse(code=10509, msg='batch create variable failed')
        return JsonResponse(data=serializer.data)
