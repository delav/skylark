from io import BytesIO
from loguru import logger
from django.db import transaction
from django.db.models import Q
from django.core.files.base import ContentFile
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from infra.utils.imagegenerator import ImageGenerator
from infra.django.response import JsonResponse
from application.status import KeywordType, ModuleStatus, KeywordGroupType
from application.common.keyword.formatter import format_keyword_data
from application.manager import get_project_by_id
from application.mapping import module_status_map
from application.storage import update_lib_keyword_storage
from application.keywordgroup.models import KeywordGroup
from application.keywordgroup.serializers import KeywordGroupSerializers
from application.libkeyword.models import LibKeyword
from application.libkeyword.serializers import LibKeywordSerializers
from application.libkeyword.handler import get_last_library_info, scan_keyword
from application.usergroup.models import Group
from application.pythonlib.models import PythonLib

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

    def create(self, request, *args, **kwargs):
        logger.info(f'create keyword: {request.data}')
        image_name = request.data.get('name') + '.png'
        if request.data.get('image'):
            img = bytes(request.data.get('image'))
        else:
            img = ImageGenerator.generate(128, image_name, 'PNG')
        image_file = ContentFile(BytesIO(img).getvalue(), image_name)
        request.data['image'] = image_file
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group_id = serializer.validated_data.get('group_id')
        keyword_group_query = KeywordGroup.objects.filter(id=group_id)
        if not keyword_group_query.exists():
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        user_group_ids = Group.objects.filter(
            user=request.user
        ).values_list('id')
        user_group_id = keyword_group_query.first().user_group_id
        if not request.user.is_staff and (user_group_id,) not in user_group_ids:
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        self.perform_create(serializer)
        instance = serializer.save()
        update_lib_keyword_storage(LibKeyword, instance.id)
        return JsonResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update keyword: {request.data}')
        instance = self.get_object()
        if request.data.get('image'):
            name = request.data.get('name') or instance.name
            img = bytes(request.data.get('image'))
            image_file = ContentFile(BytesIO(img).getvalue(), name+'.png')
            request.data['image'] = image_file
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        group_id = serializer.validated_data.get('group_id')
        keyword_group_query = KeywordGroup.objects.filter(id=group_id)
        if not keyword_group_query.exists():
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        user_group_ids = Group.objects.filter(
            user=request.user
        ).values_list('id')
        user_group_id = keyword_group_query.first().user_group_id
        if not request.user.is_staff and (user_group_id,) not in user_group_ids:
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        self.perform_update(serializer)
        update_lib_keyword_storage(LibKeyword, instance.id)
        return JsonResponse(serializer.data)

    @action(methods=['get'], detail=False)
    def get_list_by_group(self, request, *args, **kwargs):
        logger.info(f'get keyword group by group id: {request.query_params}')
        keyword_group_id = request.query_params.get('group')
        keyword_group_query = KeywordGroup.objects.filter(
            id=keyword_group_id
        )
        if not keyword_group_query.exists():
            return JsonResponse(code=10503, msg='query failed')
        user_group_ids = Group.objects.filter(
            user=request.user
        ).values_list('id')
        user_group_id = keyword_group_query.first().user_group_id
        if not request.user.is_staff and (user_group_id,) not in user_group_ids:
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        queryset = LibKeyword.objects.filter(
            group_id=keyword_group_id
        )
        library_queryset = PythonLib.objects.filter(
            user_group_id=user_group_id
        )
        library_map = {t.id: t.lib_name for t in library_queryset}
        group_keywords = []
        for item in queryset.iterator():
            data = self.get_serializer(item).data
            data['status_desc'] = module_status_map.get(data['status'])
            data['library_name'] = library_map.get(item.library_id)
            group_keywords.append(data)
        return JsonResponse(data=group_keywords)

    @action(methods=['get'], detail=False)
    def scan_keyword(self, request, *args, **kwargs):
        logger.info('scan keyword file by team')
        if request.user.is_staff:
            user_group_queryset = Group.objects.all()
            group_id_list = [g.id for g in user_group_queryset]
        else:
            user_group_query = Group.objects.filter(
                user=request.user
            )
            user_group = user_group_query.first()
            group_id_list = [user_group.id]
        operation_libraries = get_last_library_info(group_id_list)
        # update python library info
        try:
            with transaction.atomic():
                for operation, operation_list in operation_libraries.items():
                    if operation == 'delete' and operation_list:
                        for instance in operation_list:
                            instance.delete()
                    if operation == 'update' and operation_list:
                        PythonLib.objects.bulk_update(operation_list)
                    if operation == 'create' and operation_list:
                        PythonLib.objects.bulk_create(operation_list)
        except (Exception,) as e:
            logger.warning(f'update group library failed: {e}')
            return JsonResponse(code=10501, msg='scan library failed')
        ready_keywords = scan_keyword(group_id_list, True)
        return JsonResponse(data=ready_keywords)


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
