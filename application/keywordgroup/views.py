from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from infra.django.response import JsonResponse
from application.keywordgroup.models import KeywordGroup
from application.keywordgroup.serializers import KeywordGroupSerializers

# Create your views here.


class KeywordGroupViewSets(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                           mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = KeywordGroup.objects.all()
    serializer_class = KeywordGroupSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get all keyword group')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        logger.info(f'create keyword group: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except Exception as e:
            logger.error(f'create keyword group failed: {e}')
            return JsonResponse(code=10101, msg='create test case failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update keyword group: {request.data}')
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except (Exception,):
            return JsonResponse(code=10102, msg='keyword group not found')
        return JsonResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
