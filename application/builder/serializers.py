from rest_framework import serializers
from application.builder.models import Builder


class BuilderSerializers(serializers.ModelSerializer):
    
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    build_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Builder
        fields = '__all__'


class BuildDataSerializers(serializers.ModelSerializer):

    project_id = serializers.IntegerField(required=True)
    project_name = serializers.CharField(required=True)
    online = serializers.BooleanField(required=True, help_text='run data from web or db')
    run_data = serializers.ListField(required=True, help_text='detail data or module ids')

    class Meta:
        model = Builder
        fields = ('cron_job', 'debug', 'env', 'project_id', 'project_name', 'online', 'run_data')