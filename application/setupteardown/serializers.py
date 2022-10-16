from rest_framework import serializers
from application.setupteardown.models import SetupTeardown


class SetupTeardownSerializers(serializers.ModelSerializer):

    class Meta:
        model = SetupTeardown
        fields = '__all__'

