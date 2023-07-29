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
    from_region_id = serializers.IntegerField(required=False, help_text='copied region id')
    to_env_id = serializers.IntegerField(help_text='new env id')
    to_region_id = serializers.IntegerField(required=False, help_text='new region id')
    variable_id_list = serializers.ListField(required=False, help_text='variable id list')

    class Meta:
        model = Variable
        fields = (
            'module_id', 'module_type',
            'from_env_id', 'from_region_id', 'to_env_id', 'to_region_id', 'variable_id_list'
        )
