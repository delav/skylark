from rest_framework import serializers
from application.suitedir.models import SuiteDir


class SuiteDirSerializers(serializers.ModelSerializer):

    project_id = serializers.IntegerField(help_text='associated project id')
    parent_dir_id = serializers.IntegerField(help_text='parent dir id')

    class Meta:
        model = SuiteDir
        fields = (
            'id', 'name', 'document', 'category', 'create_at',
            'update_at', 'create_by', 'update_by', 'parent_dir_id', 'project_id', 'status'
        )
        read_only_fields = ('category', 'status', 'create_by', 'update_by')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        if not request:
            return ret
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == 'PUT':
            # not allowed update project id
            del attrs['project_id']
        return attrs
