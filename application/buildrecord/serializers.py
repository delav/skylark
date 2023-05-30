from rest_framework import serializers
from application.buildrecord.models import BuildRecord


class BuildRecordSerializers(serializers.ModelSerializer):

    class Meta:
        model = BuildRecord
        fields = '__all__'


