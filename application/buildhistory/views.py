from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from application.infra.django.response import JsonResponse
from application.buildhistory.models import BuildHistory
from application.buildhistory.serializers import BuildHistorySerializers

# Create your views here.


class BuildHistoryViewSets(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BuildHistory.objects.all()
    serializer_class = BuildHistorySerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get history by record id: {request.query_params}')
        try:
            record_id = request.query_params.get('record')
            queryset = BuildHistory.objects.filter(
                record_id=record_id
            )
            data = self.get_serializer(queryset, many=True).data
            return JsonResponse(data=data)
        except (Exception,) as e:
            logger.error(f'get history failed: {e}')
            return JsonResponse(code=10500, msg='get history failed')

    def retrieve(self, request, *args, **kwargs):
        pass
