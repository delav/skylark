from rest_framework import serializers
from application.environment.models import Environment


class EnvironmentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Environment
        fields = '__all__'
