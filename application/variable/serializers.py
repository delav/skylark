from rest_framework import serializers
from application.variable.models import Variable


class VariableSerializers(serializers.ModelSerializer):
    edit = serializers.BooleanField(read_only=True)

    class Meta:
        model = Variable
        fields = '__all__'

    def to_representation(self, instance):
        instance.edit = False
        return super().to_representation(instance)


class BatchVariableSerializers(serializers.ModelSerializer):
    variable_list = serializers.ListField(help_text='variable list')
    env_id = serializers.IntegerField(required=False)
    region_id = serializers.IntegerField(required=False)

    class Meta:
        model = Variable
        fields = ('variable_list', 'env_id', 'region_id')
