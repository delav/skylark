from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.buildhistory.models import BuildHistory
from application.buildhistory.serializers import BuildHistorySerializers

# Create your views here.


class BuildHistoryViewSets(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = BuildHistory.objects.all()
    serializer_class = BuildHistorySerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get history by record id: {request.query_params}')
        record_id = request.query_params.get('record')
        queryset = BuildHistory.objects.filter(
            record_id=record_id
        )
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

