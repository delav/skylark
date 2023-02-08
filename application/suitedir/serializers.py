from rest_framework import serializers
from application.suitedir.models import SuiteDir
from application.tag.serializers import TagSerializers


class SuiteDirSerializers(serializers.ModelSerializer):

    parent_dir_id = serializers.IntegerField(allow_null=True)
    project_id = serializers.IntegerField()
    tags = TagSerializers(many=True, required=False)

    class Meta:
        model = SuiteDir
        fields = ('id', 'name', 'document', 'category', 'tags', 'parent_dir_id', 'project_id')
