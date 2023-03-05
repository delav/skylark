from rest_framework import serializers
from application.tag.models import Tag


class TagSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
