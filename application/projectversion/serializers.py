from rest_framework import serializers
from application.projectversion.models import ProjectVersion


class ProjectVersionSerializers(serializers.ModelSerializer):
    version = serializers.CharField(required=False, help_text='commit version')

    class Meta:
        model = ProjectVersion
        fields = (
            'id', 'project_id', 'branch', 'total_case', 'version',
            'nodes', 'remark', 'create_at', 'update_at', 'create_by', 'update_by', 'status'
        )
        read_only_fields = ('nodes', 'status', 'create_by', 'update_by')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret
