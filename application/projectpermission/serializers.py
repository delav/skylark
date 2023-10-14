from rest_framework import serializers
from application.projectpermission.models import ProjectPermission


class ProjectPermissionSerializers(serializers.ModelSerializer):

    action_type = serializers.ChoiceField(choices=[1, 2], help_text='1: add, 2: delete')

    class Meta:
        model = ProjectPermission
        fields = (
            'user_id', 'project_id', 'action_type'
        )
