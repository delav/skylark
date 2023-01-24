from rest_framework import serializers
from application.variable.models import Variable


class VariableSerializers(serializers.ModelSerializer):
    edit = serializers.BooleanField(read_only=True)

    class Meta:
        model = Variable
        fields = '__all__'
