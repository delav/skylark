from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.pagination.paginator import PagePagination
from infra.django.response import JsonResponse
from application.constant import ModuleStatus
from application.manager import get_department_list, get_user_group_list
from application.usergroup.models import UserGroup
from application.project.models import Project
from application.projectpermission.models import ProjectPermission
from application.project.serializers import ProjectSerializers
from application.common.operator import ProjectCopyOperator, ProjectDeleteOperator
from application.common.access.projectaccess import has_project_permission
from application.common.access.projectaccess import add_self_project_permission, add_group_project_permission
# Create your views here.


class ProjectViewSets(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get project list info')
        user_project_ids = ProjectPermission.objects.filter(
            user_id=request.user.id
        ).values_list('project_id').all()
        common_project_queryset = Project.objects.filter(
            status=ModuleStatus.NORMAL,
            personal=False,
            id__in=user_project_ids
        )
        personal_project_queryset = Project.objects.filter(
            status=ModuleStatus.NORMAL,
            personal=True,
            create_by=request.user.email
        )
        project_queryset = common_project_queryset | personal_project_queryset
        project_list = ProjectSerializers(project_queryset, many=True).data
        return JsonResponse(data=project_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'create project: {request.data}')
        cname = request.data.get('cname')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_name = serializer.validated_data.get('name')
        _project = Project.objects.filter(name=project_name)
        if _project.exists():
            return JsonResponse(code=10080, msg='project name already exist')
        current_user = request.user
        if cname:
            copied_project_queryset = Project.objects.filter(
                name=cname,
                status=ModuleStatus.NORMAL
            )
            if not copied_project_queryset.exists():
                return JsonResponse(code=10088, msg='copy project not exist')
            copied_project = copied_project_queryset.first()
            if not has_project_permission(copied_project.id, current_user):
                return JsonResponse(code=40300, msg='403_FORBIDDEN')
        else:
            copied_project = Project.objects.filter(
                name=settings.PROJECT_MODULE,
                status=ModuleStatus.NORMAL
            ).first()
        groups_queryset = current_user.groups.all()
        user_group_id = groups_queryset.first().id
        is_personal = serializer.validated_data.get('personal')
        operator = ProjectCopyOperator(
            project_name,
            copied_project,
            create_by=current_user.email,
            group_id=user_group_id,
            personal=is_personal
        )
        with transaction.atomic():
            operator.copy_project_action() if cname else operator.new_project_action()
            project = operator.get_new_project()
            if is_personal:
                add_self_project_permission(project.id, current_user)
            else:
                add_group_project_permission(project.id, current_user)
        result_serializer = self.get_serializer(project)
        return JsonResponse(data=result_serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update project: {request.data}')
        instance = self.get_object()
        if instance.status != ModuleStatus.NORMAL:
            return JsonResponse(code=10088, msg='project not exist')
        if not has_project_permission(instance.id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        update_data = request.data
        # only allowed update personal project to group project
        if 'personal' in update_data:
            update_data['personal'] = False
        serializer = self.get_serializer(instance, data=update_data)
        serializer.is_valid(raise_exception=True)
        new_personal = serializer.validated_data.get('personal')
        with transaction.atomic():
            self.perform_update(serializer)
            # change personal project to group project
            if instance.personal and not new_personal:
                add_group_project_permission(instance.id, request.user)
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete project: {kwargs.get("pk")}')
        instance = self.get_object()
        if not has_project_permission(instance.id, request.user):
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        delete_operator = ProjectDeleteOperator(instance.id, request.user.email)
        delete_operator.delete_project()
        return JsonResponse(data=instance.id)

    @action(methods=['get'], detail=False)
    def tree(self, request, *args, **kwargs):
        logger.info(f'get project tree')
        department_map = {}
        for item in get_department_list():
            # add leaf field for el-tree
            item['leaf'] = False
            department_map[item['id']] = item
        group_map = {}
        for item in get_user_group_list():
            # add leaf field for el-tree
            item['leaf'] = False
            group_map[item['id']] = item
        common_project_queryset = Project.objects.filter(
            status=ModuleStatus.NORMAL,
            personal=False
        )
        personal_project_queryset = Project.objects.filter(
            status=ModuleStatus.NORMAL,
            personal=True,
            create_by=request.user.email
        )
        project_queryset = common_project_queryset | personal_project_queryset
        for project in project_queryset:
            group_id = project.group_id
            if group_id not in group_map:
                continue
            if 'children' not in group_map[group_id]:
                group_map[group_id]['children'] = []
            group_map[group_id]['children'].append(ProjectSerializers(project).data)
        for group_id, group in group_map.items():
            department_id = group['department_id']
            if department_id not in department_map:
                continue
            if 'children' not in department_map[department_id]:
                department_map[department_id]['children'] = []
            department_map[department_id]['children'].append(group)
        project_tree = department_map.values()
        return JsonResponse(data=project_tree)


class AdminProjectViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers
    pagination_class = PagePagination

    def list(self, request, *args, **kwargs):
        logger.info('get project list by admin')
        queryset = self.get_queryset()
        pg_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(pg_queryset, many=True)
        return JsonResponse(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete project by admin: {kwargs.get("pk")}')
        instance = self.get_object()
        self.perform_destroy(instance)
        return JsonResponse(data=instance.id)
