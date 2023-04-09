from rest_framework import serializers
from application.buildhistory.models import BuildHistory, HistoryDetail


class BuildHistorySerializers(serializers.ModelSerializer):

    class Meta:
        model = BuildHistory
        fields = '__all__'


class HistoryDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = HistoryDetail
        fields = '__all__'
