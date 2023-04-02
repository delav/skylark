from rest_framework import serializers
from application.suitedir.models import SuiteDir


class SuiteDirSerializers(serializers.ModelSerializer):

    parent_dir_id = serializers.IntegerField(allow_null=True)
    project_id = serializers.IntegerField()
    create_by = serializers.CharField(source='create_by.email')
    update_by = serializers.CharField(source='update_by.email')

    class Meta:
        model = SuiteDir
        fields = (
            'id', 'name', 'document', 'category', 'create_at',
            'update_at', 'create_by', 'update_by', 'parent_dir_id', 'project_id'
        )

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user
        attrs['update_by'] = request.user
        return attrs
