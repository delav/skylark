from rest_framework import serializers
from application.buildplan.models import BuildPlan


class BuildPlanSerializers(serializers.ModelSerializer):
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = BuildPlan
        fields = (
            'id', 'total_case', 'create_at', 'update_at', 'create_by', 'update_by',
            'timer_task', 'envs', 'project_id', 'extra_data'
        )

