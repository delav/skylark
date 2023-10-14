from loguru import logger
from rest_framework import mixins
from rest_framework import viewsets
from django.contrib.auth.models import Group
from infra.django.response import JsonResponse
from application.constant import ModuleStatus
from application.manager import get_department_list, get_user_group_list, get_user_info_by_uid
from application.projectpermission.models import ProjectPermission
from application.projectpermission.serializers import ProjectPermissionSerializers
from application.project.models import Project
from application.project.serializers import ProjectSerializers

# Create your views here.


class ProjectPermissionViewSets(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ProjectPermission.objects.all()
    serializer_class = ProjectPermissionSerializers

    def list(self, request, *args, **kwargs):
        logger.info('get current user edit permission project')
        group_query = Group.objects.filter(
            user=request.user
        )
        if not group_query.exists():
            return JsonResponse(code=10089, msg='Not found user group')
        group = group_query.first()
        common_project_queryset = Project.objects.filter(
            status=ModuleStatus.NORMAL,
            personal=False,
            group_id=group.id
        )
        common_project_list = ProjectSerializers(common_project_queryset, many=True).data
        department_map = {}
        for item in get_department_list():
            department_map[item['id']] = item
        group_map = {}
        for item in get_user_group_list():
            group_map[item['id']] = item
        for project in common_project_list:
            permission_project_queryset = ProjectPermission.objects.filter(
                project_id=project['id']
            )
            permission_user_list = [get_user_info_by_uid(item.user_id) for item in permission_project_queryset]
            project['user_list'] = permission_user_list
        personal_project_queryset = Project.objects.filter(
            status=ModuleStatus.NORMAL,
            personal=True,
            create_by=request.user.email
        )
        personal_project_list = ProjectSerializers(personal_project_queryset, many=True).data
        project_list = common_project_list + personal_project_list
        return JsonResponse(data=project_list)

    def create(self, request, *args, **kwargs):
        logger.info(f'update user permission project: {request.data}')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Group.objects.get(
            user=request.user
        )
        data = serializer.validated_data
        project = Project.objects.get(id=data.get('project_id'))
        if project.group_id != group.id:
            return JsonResponse(code=40300, msg='403_FORBIDDEN')
        permission_query = ProjectPermission.objects.filter(
            user_id=data.get('user_id'),
            project_id=data.get('project_id'),
        )
        if data.get('action_type') == 1:
            if permission_query.exists():
                return JsonResponse(code=10088, msg='user already had permission')
            ProjectPermission.objects.create(
                user_id=data.get('user_id'),
                project_id=data.get('project_id')
            )
        elif data.get('action_type') == 2:
            if not permission_query.exists():
                return JsonResponse(code=10088, msg='user have not permission')
            permission_query.delete()
        return JsonResponse(msg='operate success')
