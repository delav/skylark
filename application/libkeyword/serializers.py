from rest_framework import serializers
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):

    class Meta:
        model = LibKeyword
        fields = '__all__'
        extra_kwargs = {
            'create_at': {'read_only': True},
            'update_at': {'read_only': True},
        }
