from rest_framework import serializers
from application.builder.models import Builder


class TestInstantBuildSerializers(serializers.ModelSerializer):

    plan_id = serializers.IntegerField(help_text='build plan id')
    env_list = serializers.ListField(help_text='build env ids')
    region_list = serializers.ListField(help_text='build region ids')
    action_type = serializers.CharField(help_text='start or stop')

    class Meta:
        model = Builder
        fields = (
            'plan_id', 'env_list', 'region_list', 'action_type'
        )


class TestQuickBuildSerializers(serializers.ModelSerializer):

    project_id = serializers.IntegerField(help_text='build plan id')
    project_name = serializers.CharField(help_text='build env id')
    branch = serializers.CharField(help_text='build region id')
    env_list = serializers.ListField(help_text='build env ids')
    region_list = serializers.ListField(help_text='build region ids')
    case_list = serializers.ListField(help_text='build case ids')
    action_type = serializers.CharField(help_text='start or stop')

    class Meta:
        model = Builder
        fields = (
            'project_id', 'project_name', 'branch', 'env_list', 'region_list', 'case_list', 'action_type'
        )


class DebugBuildSerializers(serializers.ModelSerializer):

    action_type = serializers.CharField(help_text='start or stop')
    project_id = serializers.IntegerField(help_text='build project id')
    env_id = serializers.IntegerField(help_text='build env id')
    env_name = serializers.CharField(help_text='build env name')
    region_id = serializers.IntegerField(required=False, help_text='build region id')
    region_name = serializers.CharField(required=False, help_text='build region name')
    project_name = serializers.CharField(help_text='build project name')
    run_data = serializers.ListField(help_text='detail data or module ids')

    class Meta:
        model = Builder
        fields = (
            'action_type', 'env_id', 'env_name', 'region_id', 'region_name', 'project_id', 'project_name', 'run_data'
        )
