from rest_framework import serializers
from application.project.models import Project


class ProjectSerializers(serializers.ModelSerializer):

    copy_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'project_name', 'create_at', 'create_by')

