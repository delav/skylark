from rest_framework import serializers
from application.builder.models import Builder


class BuilderSerializers(serializers.ModelSerializer):
    
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    build_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    build_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Builder
        fields = '__all__'


class BuildDataSerializers(serializers.ModelSerializer):

    project_id = serializers.IntegerField()
    env_id = serializers.IntegerField()
    project_name = serializers.CharField()
    run_data = serializers.ListField(help_text='detail data or module ids')
    timer_info = serializers.DictField(required=False, help_text='timer task info')

    class Meta:
        model = Builder
        fields = ('debug', 'env_id', 'project_id', 'project_name', 'run_data', 'timer_info')
