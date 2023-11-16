from loguru import logger
from django.conf import settings
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action


class InternalTriggerViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def build_trigger(self, request, *args, **kwargs):
        logger.info(f'build trigger: {request.data}')

