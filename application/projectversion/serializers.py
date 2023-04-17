from rest_framework import serializers
from application.projectversion.models import ProjectVersion


class ProjectVersionSerializers(serializers.ModelSerializer):

    class Meta:
        model = ProjectVersion
        fields = (
            'id', 'project_id', 'branch', 'version', 'content',
            'sources', 'remark', 'create_at', 'update_at', 'create_by', 'update_by'
        )
        read_only_fields = ('create_by', 'update_by', 'content', 'sources')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        return attrs
