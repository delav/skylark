from rest_framework import serializers
from application.workermanager.models import WorkerManager


class WorkerManagerSerializers(serializers.ModelSerializer):

    class Meta:
        model = WorkerManager
        fields = '__all__'

