from rest_framework import serializers
from application.keywordgroup.models import KeywordGroup
from application.libkeyword.serializers import LibKeywordSerializers


class KeywordGroupSerializers(serializers.ModelSerializer):

    class Meta:
        model = KeywordGroup
        fields = '__all__'
        read_only_fields = ('group_type', 'user_group_id')


class KeywordGroup2Serializers(serializers.ModelSerializer):

    keywords = LibKeywordSerializers(read_only=True, many=True)

    class Meta:
        model = KeywordGroup
        fields = ('id', 'name', 'group_type', 'project_id', 'keywords')

