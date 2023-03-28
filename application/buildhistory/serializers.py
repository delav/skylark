from rest_framework import serializers
from application.buildhistory.models import BuildHistory


class BuildHistorySerializers(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BuildHistory
        fields = '__all__'
