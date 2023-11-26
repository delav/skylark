from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.executeparam.models import ExecuteParam
from application.executeparam.serializers import ExecuteParamSerializers

# Create your views here.


class ExecuteParamViewSets(mixins.ListModelMixin, mixins.CreateModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = ExecuteParam.objects.all()
    serializer_class = ExecuteParamSerializers

    def create(self, request, *args, **kwargs):
        logger.info(f'create or update execute param: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance, created = ExecuteParam.objects.update_or_create(
            defaults=serializer.validated_data,
            project_id=serializer.validated_data.get('project_id'),
            parameters=serializer.validated_data.get('parameters')
        )
        data = self.get_serializer(instance).data if created else None
        return JsonResponse(data=data)

    def list(self, request, *args, **kwargs):
        logger.info(f'get project execute params')
        project_id = request.query_params.get('project')
        result_list = []
        if project_id and isinstance(project_id, str) and project_id.isdigit():
            project_id = int(project_id)
            queryset = self.get_queryset().filter(
                project_id=project_id
            ).order_by('-create_at')
            result_list = self.get_serializer(queryset, many=True).data
        return JsonResponse(data=result_list)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete execute param: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)
