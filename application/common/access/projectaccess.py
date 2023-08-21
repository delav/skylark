from application.user.models import User
from application.projectpermission.models import ProjectPermission


def has_project_permission(project_id, user):
    if not project_id:
        return False
    if user.is_superuser:
        return True
    permission_project = ProjectPermission.objects.filter(
        user_id=user.id,
        project_id=project_id
    )
    return permission_project.exists()


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
