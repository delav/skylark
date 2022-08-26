from rest_framework import serializers
from application.suitedir.models import SuiteDir


class SuiteDirSerializers(serializers.ModelSerializer):

    parent_dir_id = serializers.IntegerField(allow_null=True)
    project_id = serializers.IntegerField()

    class Meta:
        model = SuiteDir
        fields = ('id', 'dir_name', 'parent_dir_id', 'project_id', 'dir_type')
