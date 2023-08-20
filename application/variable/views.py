from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.variable.models import Variable
from application.variable.serializers import VariableSerializers, CopyVariableSerializers

# Create your views here.


class VariableViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get variables by module: {request.query_params}')
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
        ser = self.get_serializer(variable_queryset, many=True)
        return JsonResponse(data=ser.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create variable: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update variable: {request.data}')
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get variable: {kwargs.get("pk")}')
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete variable: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)

    @action(methods=['post'], detail=False)
    def copy(self, request, *args, **kwargs):
        logger.info(f'batch copy variables: {request.data}')
        serializer = CopyVariableSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        module_id = serializer.data.get('module_id')
        module_type = serializer.data.get('module_type')
        from_env_id = serializer.data.get('from_env_id')
        from_region_id = serializer.data.get('from_region_id')
        to_env_id = serializer.data.get('to_env_id')
        to_region_id = serializer.data.get('to_region_id')
        variable_id_list = serializer.data.get('variable_id_list')
        params = {
            'module_id': module_id,
            'module_type': module_type,
            'env_id': from_env_id
        }
        if from_region_id:
            params['region_id'] = from_region_id
        if variable_id_list:
            params['id__in'] = variable_id_list
        copied_variables = Variable.objects.filter(
            **params
        )
        copy_create_list = []
        for item in copied_variables.iterator():
            new_item = VariableSerializers(item).data
            del new_item['id']
            new_item['env_id'] = to_env_id
            if to_region_id:
                new_item['region_id'] = to_region_id
            obj = Variable(**new_item)
            copy_create_list.append(obj)
        Variable.objects.bulk_create(copy_create_list)
        return JsonResponse(data='success')
