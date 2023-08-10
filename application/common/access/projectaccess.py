from rest_framework.permissions import BasePermission
from application.user.models import User
from application.usergroup.models import UserGroup
from application.project.models import Project


class ProjectAccess(BasePermission):

    def has_permission(self, request, view):
        project_id = request.data.get('project_id')
        if not project_id:
            return False
        groups_queryset = UserGroup.objects.filter(
            user=request.user
        )
        users = User.objects.none()
        for group in groups_queryset:
            users |= group.user_set.all()
        group_emails = [user.email for user in users]
        projects = Project.objects.filter(
            project_id=project_id,
            create_by__in=group_emails
        )
        return projects.exists()

