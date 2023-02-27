from rest_framework import serializers
from application.projectversion.models import ProjectVersion


class ProjectVersionSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProjectVersion
        fields = '__all__'
