from django.db.models import Q
from application.status import ModuleStatus
from application.environment.models import Environment
from application.environment.serializers import EnvironmentSerializers
from application.region.models import Region
from application.region.serializers import RegionSerializers
from application.project.models import Project
from application.project.serializers import ProjectSerializers
from application.projectpermission.models import ProjectPermission
from application.user.models import User
from application.user.serializers import UserSerializer
from application.usergroup.models import UserGroup
from application.usergroup.serializers import UserGroupSerializers
from application.department.models import Department
from application.department.serializers import DepartmentSerializers
from application.pythonlib.models import PythonLib
from application.pythonlib.serializers import PythonLibSerializers


def get_env_list():
    env_query = Environment.objects.filter(
        status=ModuleStatus.NORMAL
    )
    return EnvironmentSerializers(env_query, many=True).data


def get_region_list():
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


def get_department_list():
    department_queryset = Department.objects.all()
    return DepartmentSerializers(department_queryset, many=True).data


def get_user_group_list():
    user_group_queryset = UserGroup.objects.select_related('group').all()
    return UserGroupSerializers(user_group_queryset, many=True).data


def get_user_list():
    user_query = User.objects.all()
    return UserSerializer(user_query, many=True).data


def get_user_info_by_uid(user_id):
    user = User.objects.get(id=user_id)
    user_group_query = UserGroup.objects.filter(
        group__user__id=user_id
    ).select_related('group')
    user_group = user_group_query.first()
    department = Department.objects.get(id=user_group.department_id)
    user_data = UserSerializer(user).data
    user_data.update({
        'group_id': user_group.group.id,
        'group_name': user_group.group.name,
        'department_id': department.id,
        'department_name': department.name
    })
    return user_data


def get_group_library_list(group_id):
    library_queryset = PythonLib.objects.filter(
        Q(user_group_id=group_id) | Q(user_group_id=None)
    )
    return PythonLibSerializers(library_queryset, many=True).data
