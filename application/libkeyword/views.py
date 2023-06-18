from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from infra.django.response import JsonResponse
from application.constant import KeywordType, ModuleStatus
from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers
from application.common.keyword.formatkeyword import format_keyword_data

# Create your views here.


class LibKeywordViewSets(mixins.ListModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = LibKeyword.objects.all()
    serializer_class = LibKeywordSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get all lib keywords')
        queryset = LibKeyword.objects.filter(status=ModuleStatus.NORMAL)
        lib_keywords = []
        lib_type = KeywordType.LIB
        for item in queryset.iterator():
            serializer = self.get_serializer(item)
            keyword_data = format_keyword_data(
                **serializer.data,
                keyword_type=lib_type
            )
            lib_keywords.append(keyword_data)
        return JsonResponse(data=lib_keywords)

    def create(self, request, *args, **kwargs):
        logger.info(f'add lib keyword: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except (Exception,) as e:
            logger.error(f'save lib keyword failed: {e}')
            return JsonResponse(code=10024, msg='create lib keyword failed')
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update lib keyword: {request.data}')
        update_data = self.request.data
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=update_data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except (Exception,) as e:
            logger.error(f'update lib keyword error: {e}')
            return JsonResponse(code=10023, msg='update lib keyword failed')
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete lib keyword: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete lib keyword error: {e}')
            return JsonResponse(code=10022, msg='delete lib keyword failed')
        return JsonResponse(data=instance.id)

    def get_permissions(self):
        if self.request.method in ('POST', 'UPDATE', 'DELETE'):
            return [IsAdminUser()]
        return [permission() for permission in self.permission_classes]
