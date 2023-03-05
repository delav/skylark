from rest_framework import serializers
from application.casepriority.models import CasePriority


class CasePrioritySerializers(serializers.ModelSerializer):

    class Meta:
        model = CasePriority
        fields = '__all__'
