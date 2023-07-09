from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from infra.django.response import JsonResponse
from application.constant import KeywordType, ModuleStatus, KeywordGroupType
from application.keywordgroup.models import KeywordGroup
from application.keywordgroup.serializers import KeywordGroupSerializers
from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers
from application.common.keyword.formatkeyword import format_keyword_data

# Create your views here.


class LibKeywordViewSets(viewsets.GenericViewSet):

    @action(methods=['post'], detail=False)
    def get_keyword_list(self, request, *args, **kwargs):
        logger.info('get lib keywords by group type')
        is_base = request.data.get('base', True)
        if is_base:
            group_queryset = KeywordGroup.objects.filter(
                group_type=KeywordGroupType.LIB
            )
        else:
            group_queryset = KeywordGroup.objects.filter().exclude(
                group_type__in=[KeywordGroupType.LIB, KeywordGroupType.USER]
            )
        group_map = {}
        group_id_list = []
        for group in group_queryset.iterator():
            group_data = KeywordGroupSerializers(group, context={'request': request}).data
            group_data['keywords'] = []
            group_id_list.append(group.id)
            group_map[group.id] = group_data
        keyword_queryset = LibKeyword.objects.filter(
            group_id__in=group_id_list,
            status=ModuleStatus.NORMAL
        )
        for item in keyword_queryset.iterator():
            serializer = LibKeywordSerializers(item, context={'request': request})
            keyword_data = format_keyword_data(
                **serializer.data,
                keyword_type=KeywordType.LIB
            )
            group_map[item.group_id]['keywords'].append(keyword_data)
        return JsonResponse(data=group_map.values())


class AdminKeywordViewSets(mixins.ListModelMixin, mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = LibKeyword.objects.all()
    serializer_class = LibKeywordSerializers
    permission_classes = (IsAdminUser,)

    def list(self, request, *args, **kwargs):
        logger.info('get all lib keywords')
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)

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