from rest_framework import serializers
from application.project.models import Project


class ProjectSerializers(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'create_at', 'update_at', 'create_by')

