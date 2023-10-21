from loguru import logger
from rest_framework import viewsets
from rest_framework.decorators import action
from infra.django.response import JsonResponse
from application.constant import ModuleStatus
from application.manager import get_env_list, get_region_list
from application.manager import get_department_list, get_user_group_list, get_user_list
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.projectpermission.models import ProjectPermission


class BaseViewSets(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def base_info(self, request, *args, **kwargs):
        logger.info(f'get project related info')
        base_info = {
            'env_list': get_env_list(),
            'region_list': get_region_list(),
            'project_list': []
        }
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
        base_info['project_list'] = ProjectSerializers(project_queryset, many=True).data
        return JsonResponse(data=base_info)

    @action(methods=['get'], detail=False)
    def project_info(self, request, *args, **kwargs):
        logger.info(f'get project related info')
        project_info = {
            'department_list': get_department_list(),
            'group_list': get_user_group_list(),
            'project_list': []
        }
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
        project_info['project_list'] = ProjectSerializers(project_queryset, many=True).data
        return JsonResponse(data=project_info)
