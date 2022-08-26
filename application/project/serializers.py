from rest_framework import serializers
from application.project.models import Project


class ProjectSerializers(serializers.ModelSerializer):
    create_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Project
        fields = ('id', 'name', 'create_at', 'create_by')

