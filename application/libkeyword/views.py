from io import BytesIO
from loguru import logger
from django.db.models import Q
from django.core.files.base import ContentFile
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from infra.utils.imagegenerator import ImageGenerator
from infra.django.response import JsonResponse
from application.constant import KeywordType, ModuleStatus, KeywordGroupType
from application.keywordgroup.models import KeywordGroup
from application.keywordgroup.serializers import KeywordGroupSerializers
from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers
from application.common.keyword.formatter import format_keyword_data
from application.manager import get_project_by_id

# Create your views here.


class LibKeywordViewSets(mixins.ListModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = LibKeyword.objects.all()
    serializer_class = LibKeywordSerializers

    def list(self, request, *args, **kwargs):
        logger.info(f'get lib keywords by project: {request.query_params}')
        project_id = request.query_params.get('project')
        project = get_project_by_id(project_id)
        if not project:
            return JsonResponse(data=[])
        user_group_id = project.get('group_id')
        # lib's keyword group
        group_queryset = KeywordGroup.objects.filter(
            group_type=KeywordGroupType.PUBLIC
        )
        # team's or project's keyword group
        user_group_queryset = KeywordGroup.objects.filter(
            Q(project_id=project_id) | Q(user_group_id=user_group_id)
        )
        group_queryset |= user_group_queryset
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
            if not keyword_data:
                continue
            group_map[item.group_id]['keywords'].append(keyword_data)
        return JsonResponse(data=group_map.values())

    @action(methods=['get'], detail=False)
    def get_list_by_group(self, request, *args, **kwargs):
        logger.info(f'get keyword group by group id: {request.query_params}')
        group_id = request.query_params.get('group')
        queryset = LibKeyword.objects.filter(
            group_id=group_id
        )
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse(data=serializer.data)


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
        save_data = serializer.validated_data
        image_name = save_data.get('name') + '.png'
        img = ImageGenerator.generate(128, image_name, 'PNG')
        # gen_image = Image.open(BytesIO(img))
        # image_path = settings.KEYWORD_ICON_PATH / image_name
        # # gen_image.save(image_path)
        image_file = ContentFile(BytesIO(img).getvalue(), image_name)
        save_data['image'] = image_file
        instance = LibKeyword.objects.create(**save_data)
        data = self.get_serializer(instance).data
        return JsonResponse(data=data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update lib keyword: {request.data}')
        update_data = self.request.data
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=update_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete lib keyword: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)
