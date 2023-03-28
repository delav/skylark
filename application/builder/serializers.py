from rest_framework import serializers
from application.builder.models import Builder


class TestBuildSerializers(serializers.ModelSerializer):

    plan_id = serializers.IntegerField(help_text='build plan id')
    env_id = serializers.IntegerField(help_text='build env id')
    action_type = serializers.CharField(help_text='start or stop')

    class Meta:
        model = Builder
        fields = (
            'plan_id', 'env_id', 'action_type'
        )


class DebugBuildSerializers(serializers.ModelSerializer):

    action_type = serializers.CharField(help_text='start or stop')
    project_id = serializers.IntegerField(help_text='build project id')
    env_id = serializers.IntegerField(help_text='build env id')
    project_name = serializers.CharField(help_text='build project name')
    run_data = serializers.ListField(help_text='detail data or module ids')

    class Meta:
        model = Builder
        fields = (
            'action_type', 'env_id', 'project_id', 'project_name', 'run_data'
        )
