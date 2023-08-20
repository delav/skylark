from application.project.models import Project
from application.projectpermission.models import ProjectPermission


def has_project_permission(project_id, user):
    if not project_id:
        return False
    permission_project_ids = ProjectPermission.objects.filter(
        user_id__exact=user.id
    ).values_list('project_id').all()
    personal_project = Project.objects.filter(
        id=project_id,
        personal=True,
        create_by=user.email
    )
    return project_id not in permission_project_ids and not personal_project.exists()

