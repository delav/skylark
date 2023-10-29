from loguru import logger
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse


class StatisticsViewSets(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def case_info(self, request, *args, **kwargs):
        logger.info('get statistics case data')
        return JsonResponse(data={})

    @action(methods=['get'], detail=False)
    def build_info(self, request, *args, **kwargs):
        logger.info('get statistics build data')
        return JsonResponse(data={})
