from rest_framework import serializers
from application.builder.models import Builder


class TestInstantBuildSerializers(serializers.ModelSerializer):

    plan_id = serializers.IntegerField(help_text='build plan id')
    env_list = serializers.ListField(required=False, help_text='build env ids')
    region_list = serializers.ListField(required=False, help_text='build region ids')

    class Meta:
        model = Builder
        fields = (
            'plan_id', 'env_list', 'region_list'
        )


class TestQuickBuildSerializers(serializers.ModelSerializer):

    project_id = serializers.IntegerField(help_text='build project id')
    project_name = serializers.CharField(help_text='build project name')
    branch = serializers.CharField(help_text='project branch')
    env_list = serializers.ListField(help_text='build env id list')
    region_list = serializers.ListField(required=False, help_text='build region id list')
    parameters = serializers.CharField(required=False, help_text='run parameters')
    case_list = serializers.ListField(help_text='build case ids')

    class Meta:
        model = Builder
        fields = (
            'project_id', 'project_name', 'branch', 'env_list', 'region_list', 'parameters', 'case_list'
        )


class DebugBuildSerializers(serializers.ModelSerializer):

    project_id = serializers.IntegerField(help_text='build project id')
    project_name = serializers.CharField(help_text='build project name')
    env_id = serializers.IntegerField(help_text='build env id')
    env_name = serializers.CharField(help_text='build env name')
    region_id = serializers.IntegerField(required=False, help_text='build region id')
    region_name = serializers.CharField(required=False, help_text='build region name')
    parameters = serializers.CharField(required=False, allow_blank=True, help_text='run parameters')
    run_data = serializers.ListField(help_text='detail data or module ids')

    class Meta:
        model = Builder
        fields = (
            'project_id', 'project_name', 'env_id', 'env_name', 'region_id', 'region_name', 'parameters', 'run_data'
        )
