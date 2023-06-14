from rest_framework import serializers
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, help_text='keyword icon')

    class Meta:
        model = LibKeyword
        exclude = ('create_at', 'update_at')
