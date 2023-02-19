from rest_framework import serializers
from application.tag.models import Tag


class TagSerializers(serializers.ModelSerializer):
    project_id = serializers.IntegerField(required=False)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'project_id')