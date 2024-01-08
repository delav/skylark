from rest_framework import serializers
from application.tag.models import Tag, ModuleTag


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ModuleTagSerializers(serializers.ModelSerializer):

    class Meta:
        model = ModuleTag
        fields = '__all__'


class ModuleTagCreateSerializers(serializers.ModelSerializer):

    tag_name = serializers.CharField(help_text='tag name')
    project_id = serializers.IntegerField(help_text='associated project id')

    class Meta:
        model = ModuleTag
        fields = ('id', 'tag_name', 'project_id', 'module_id', 'module_type')
