from rest_framework import serializers
from application.project.models import Project


class ProjectSerializers(serializers.ModelSerializer):

    create_by = serializers.CharField(read_only=True)
    update_by = serializers.CharField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'create_at', 'update_at', 'create_by', 'update_by')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        return attrs
