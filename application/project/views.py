import logging

from loguru import logger
from django.conf import settings
from django.db import transaction
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.utils.timehanldler import get_timestamp
from infra.django.pagination.paginator import PagePagination
from infra.django.response import JsonResponse
from application.constant import ModuleStatus
from application.usergroup.models import UserGroup
from application.department.models import Department
from application.department.serializers import DepartmentSerializers
from application.project.models import Project
from application.projectpermission.models import ProjectPermission
from application.project.serializers import ProjectSerializers
from application.common.operator import ProjectOperator
from application.common.access.projectaccess import has_project_permission

# Create your views here.


class ProjectViewSets(mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get project list info')
        try:
            user_project_ids = ProjectPermission.objects.filter(
                user_id__exact=request.user.id
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
        except (Exception,) as e:
            logger.error(f'get project list failed: {e}')
            return JsonResponse(code=10089, msg='get project failed')
        return JsonResponse(data=project_list)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        logger.info(f'create project: {request.data}')
        cname = request.data.get('cname')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_name = serializer.validated_data.get('name')
        _project = Project.objects.filter(name=project_name)
        if _project.exists():
            return JsonResponse(code=10080, data='project name already exists')
        try:
            current_user = request.user
            if cname:
                copied_project_queryset = Project.objects.filter(
                    name=cname,
                    status=ModuleStatus.NORMAL
                )
                if not copied_project_queryset.exists():
                    return JsonResponse(code=10088, data='copy project not exists')
                copied_project = copied_project_queryset.first()
                if not has_project_permission(copied_project.id, current_user):
                    return JsonResponse(code=40300, data='403_FORBIDDEN')
            else:
                copied_project = Project.objects.filter(
                    name=settings.PROJECT_MODULE,
                    status=ModuleStatus.NORMAL
                )
            groups_queryset = UserGroup.objects.filter(user=current_user)
            user_group_id = groups_queryset.first().group_id
            operator = ProjectOperator(
                project_name,
                copied_project,
                create_by=request.user.email,
                group_id=user_group_id,
                personal=serializer.validated_data.get('personal')
                )
            with transaction.atomic():
                operator.copy_project_action() if cname else operator.new_project_action()
                project = operator.get_new_project()
        except (Exception,) as e:
            logger.error(f'create project error: {e}')
            return JsonResponse(code=10081, msg='create project failed')
        result_serializer = self.get_serializer(project)
        return JsonResponse(data=result_serializer.data)

    def update(self, request, *args, **kwargs):
        logger.info(f'update project: {request.data}')
        try:
            instance = self.get_object()
            if instance.status != ModuleStatus.NORMAL:
                return JsonResponse(code=10088, data='project not exist')
            if not has_project_permission(instance.id, request.user):
                return JsonResponse(code=40300, msg='403_FORBIDDEN')
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except (Exception,) as e:
            logger.error(f'update project failed: {e}')
            return JsonResponse(code=10087, msg='update project failed')
        return JsonResponse(serializer.data)

    def destroy(self, request, *args, **kwargs):
        logger.info(f'delete project: {kwargs.get("pk")}')
        try:
            instance = self.get_object()
            if not has_project_permission(instance.id, request.user):
                return JsonResponse(code=40300, msg='403_FORBIDDEN')
            instance.status = ModuleStatus.DELETED
            instance.name = instance.name + f'-{get_timestamp(6)}'
            instance.update_by = request.user.email
            instance.save()
        except (Exception,) as e:
            logger.error(f'delete project failed: {e}')
            return JsonResponse(code=10087, msg='delete project failed')
        return JsonResponse()

    @action(methods=['get'], detail=False)
    def tree(self, request, *args, **kwargs):
        logging.info(f'get project tree')
        try:
            department_queryset = Department.objects.all()
            department_map = {item.id: DepartmentSerializers(item).data for item in department_queryset}
            group_queryset = UserGroup.objects.select_related('group').all()
            group_map = {}
            for item in group_queryset:
                item_dict = {'id': item.group.id, 'name': item.group.name, 'department_id': item.department_id}
                group_map[item.group.id] = item_dict
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
        except (Exception,) as e:
            logger.error(f'get project list failed: {e}')
            return JsonResponse(code=10089, msg='get project failed')
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
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except (Exception,) as e:
            logger.error(f'delete project error: {e}')
            return JsonResponse(code=10086, msg='delete project failed')
        return JsonResponse(data=instance.id)
