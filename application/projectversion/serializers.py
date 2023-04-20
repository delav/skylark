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

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context['request']
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret
