from rest_framework import serializers
from application.keywordgroup.models import KeywordGroup


class KeywordGroupSerializers(serializers.ModelSerializer):

    image = serializers.ImageField(required=False)

    class Meta:
        model = KeywordGroup
        fields = '__all__'
