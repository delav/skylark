from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.buildrecord.models import BuildRecord
from application.buildrecord.serializers import BuildRecordSerializers

# Create your views here.


class BuildRecordViewSets(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BuildRecord.objects.all()
    serializer_class = BuildRecordSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get record by param: {request.query_params}')
        try:
            limit = request.query_params.get('limit', 10)
            limit = int(limit)
            queryset = BuildRecord.objects.all().order_by('-create_at')[:limit]
            data = self.get_serializer(queryset, many=True).data
            return JsonResponse(data=data)
        except (Exception,) as e:
            logger.error(f'get record failed: {e}')
            return JsonResponse(code=10400, msg='get record failed')

    def retrieve(self, request, *args, **kwargs):
        logger.info(f'get detail')

