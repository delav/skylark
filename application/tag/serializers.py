from rest_framework import serializers
from application.tag.models import Tag


class TagSerializers(serializers.ModelSerializer):
    project_id = serializers.IntegerField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'project_id', 'module_id', 'module_type')
