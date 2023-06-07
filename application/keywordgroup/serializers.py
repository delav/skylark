from rest_framework import serializers
from application.keywordgroup.models import KeywordGroup
from application.libkeyword.serializers import LibKeywordSerializers


class KeywordGroupSerializers(serializers.ModelSerializer):

    image = serializers.ImageField(required=False, help_text='keyword group icon')

    class Meta:
        model = KeywordGroup
        fields = '__all__'


class KeywordGroup2Serializers(serializers.ModelSerializer):

    keywords = LibKeywordSerializers(read_only=True, many=True)

    class Meta:
        model = KeywordGroup
        fields = ('id', 'name', 'image', 'group_type', 'keywords')

