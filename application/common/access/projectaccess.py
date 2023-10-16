from application.usergroup.models import Group
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
    groups_queryset = Group.objects.filter(user=user)
    if not groups_queryset.exists():
        return
    users = groups_queryset.first().user_set.all()
    permission_list = []
    permission_users = ProjectPermission.objects.filter(
        project_id=project_id
    )
    permission_user_list = [u.user_id for u in permission_users]
    for user in users:
        if user.id in permission_user_list:
            continue
        obj = ProjectPermission(
            user_id=user.id,
            project_id=project_id
        )
        permission_list.append(obj)
    ProjectPermission.objects.bulk_create(permission_list)
