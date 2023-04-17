from rest_framework import serializers
from application.infra.django.exception import ValidationException
from application.buildplan.models import BuildPlan


class BuildPlanSerializers(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    extra_data = serializers.JSONField(required=False)
    env_list = serializers.ListField()
    region_list = serializers.ListField(required=False)

    class Meta:
        model = BuildPlan
        fields = (
            'id', 'title', 'total_case', 'create_at', 'update_at', 'create_by',
            'update_by', 'build_cases', 'periodic_expr', 'periodic_switch',
            'env_list', 'region_list', 'project_id', 'branch', 'expect_pass', 'extra_data'
        )
        read_only_fields = ('create_by', 'update_by')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        # validate periodic
        if attrs.get('periodic_switch') and not attrs.get('periodic_expr'):
            raise ValidationException(detail='Params error', code=10110)
        return attrs

    def to_representation(self, instance: BuildPlan):
        instance.env_list = [int(i) for i in instance.envs.split(',')]
        instance.region_list = [int(i) for i in instance.regions.split(',')]
        return super(BuildPlanSerializers, self).to_representation(instance)

    def to_internal_value(self, data):
        ret = super(BuildPlanSerializers, self).to_internal_value(data)
        if ret.get('env_list'):
            ret['envs'] = ','.join(str(i) for i in ret['env_list'])
        if ret.get('region_list'):
            ret['regions'] = ','.join(str(i) for i in ret['region_list'])
        return ret
