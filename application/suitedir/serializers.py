from rest_framework import serializers
from application.suitedir.models import SuiteDir


class SuiteDirSerializers(serializers.ModelSerializer):

    parent_dir_id = serializers.IntegerField(allow_null=True)
    project_id = serializers.IntegerField()

    class Meta:
        model = SuiteDir
        fields = (
            'id', 'name', 'document', 'category', 'create_at',
            'update_at', 'create_by', 'update_by', 'parent_dir_id', 'project_id'
        )
        read_only_fields = ('create_by', 'update_by')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context['request']
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret
