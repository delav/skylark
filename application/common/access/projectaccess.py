from application.user.models import User
from application.manager import get_permission_project_by_uid
from application.projectpermission.models import ProjectPermission


def has_project_permission(project_id, user):
    project_id = int(project_id)
    if not project_id:
        return False
    if user.is_superuser:
        return True
    permission_project_list = get_permission_project_by_uid(user.id)
    return project_id in permission_project_list


def add_self_project_permission(project_id, user):
    ProjectPermission.objects.create(
        user_id=user.id,
        project_id=project_id
    )


def add_group_project_permission(project_id, user):
    groups_queryset = user.groups.all()
    users = User.objects.none()
    for group in groups_queryset:
        users |= group.user_set.all()
    permission_list = []
    for user in users:
        obj = ProjectPermission(
            user_id=user.id,
            project_id=project_id
        )
        permission_list.append(obj)
    ProjectPermission.objects.bulk_create(permission_list)
