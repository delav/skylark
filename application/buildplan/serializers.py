from rest_framework import serializers
from application.buildplan.models import BuildPlan


class BuildPlanSerializers(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    create_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    update_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    create_by = serializers.CharField(read_only=True)
    update_by = serializers.CharField(read_only=True)
    extra_data = serializers.JSONField(required=False)

    class Meta:
        model = BuildPlan
        fields = (
            'id', 'title', 'total_case', 'create_at', 'update_at', 'create_by', 'update_by',
            'periodic_expr', 'periodic_switch', 'envs', 'project_id', 'branch', 'expect_pass', 'extra_data'
        )

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        return attrs

