from rest_framework import serializers
from application.project.models import Project


class ProjectSerializers(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id', 'name', 'status', 'personal', 'group_id', 'create_at', 'update_at', 'create_by', 'update_by'
        )
        read_only_fields = ('group_id', 'status', 'create_by', 'update_by')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret
