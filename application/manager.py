from application.constant import ModuleStatus
from application.environment.models import Environment
from application.environment.serializers import EnvironmentSerializers
from application.region.models import Region
from application.region.serializers import RegionSerializers
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.projectpermission.models import ProjectPermission
from application.user.models import User
from application.user.serializers import UserSerializer


def get_all_envs():
    env_query = Environment.objects.filter(
        status=ModuleStatus.NORMAL
    )
    return EnvironmentSerializers(env_query, many=True).data


def get_all_regions():
    region_query = Region.objects.filter(
        status=ModuleStatus.NORMAL
    )
    return RegionSerializers(region_query, many=True).data


def get_project_by_id(project_id):
    project_query = Project.objects.filter(
        id=project_id,
        status=ModuleStatus.NORMAL
    )
    if not project_query.exists():
        return {}
    return ProjectSerializers(project_query.first()).data


def get_projects_by_uid(user_id):
    user_info = get_user_info_by_uid(user_id)
    user_project_ids = get_permission_project_by_uid(user_id)

    common_project_queryset = Project.objects.filter(
        status=ModuleStatus.NORMAL,
        personal=False,
        id__in=user_project_ids
    )
    personal_project_queryset = Project.objects.filter(
        status=ModuleStatus.NORMAL,
        personal=True,
        create_by=user_info.get('email')
    )
    project_queryset = common_project_queryset | personal_project_queryset
    return ProjectSerializers(project_queryset, many=True).data


def get_permission_project_by_uid(user_id):
    permission_project = ProjectPermission.objects.filter(
        user_id=user_id,
    )
    return [item.project_id for item in permission_project]


def get_all_user():
    user_query = User.objects.all()
    return UserSerializer(user_query, many=True).data


def get_user_info_by_uid(user_id):
    return {}

