from rest_framework import serializers
from application.buildhistory.models import BuildHistory, HistoryDetail


class BuildHistorySerializers(serializers.ModelSerializer):

    class Meta:
        model = BuildHistory
        exclude = ('batch', 'celery_task', 'report_path')


class HistoryDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = HistoryDetail
        fields = '__all__'
