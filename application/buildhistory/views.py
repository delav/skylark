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
        pass

    def retrieve(self, request, *args, **kwargs):
        pass
