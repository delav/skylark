from rest_framework import serializers
from application.timertask.models import TimerTask


class TimerTaskSerializers(serializers.ModelSerializer):

    class Meta:
        model = TimerTask
        fields = '__all__'

