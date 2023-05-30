from rest_framework import serializers
from application.variable.models import Variable


class VariableSerializers(serializers.ModelSerializer):
    edit = serializers.BooleanField(read_only=True, help_text='edit mode')

    class Meta:
        model = Variable
        fields = '__all__'

    def to_representation(self, instance):
        instance.edit = False
        return super().to_representation(instance)


class CopyVariableSerializers(serializers.ModelSerializer):
    module_id = serializers.IntegerField(help_text='variable module id')
    module_type = serializers.IntegerField(help_text='variable module type')
    from_env_id = serializers.IntegerField(help_text='copied env id')
    to_env_id = serializers.IntegerField(help_text='new env id')

    class Meta:
        model = Variable
        fields = ('module_id', 'module_type', 'from_env_id', 'to_env_id')
