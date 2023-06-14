from rest_framework import serializers
from infra.django.exception import ValidationException
from application.buildplan.models import BuildPlan
from infra.utils.typetransform import id_str_to_set, join_id_to_str


class BuildPlanSerializers(serializers.ModelSerializer):
    extra_data = serializers.JSONField(required=False, help_text='plan extra data')
    env_list = serializers.ListField(help_text='env id list')
    region_list = serializers.ListField(required=False, help_text='region id list')

    class Meta:
        model = BuildPlan
        fields = (
            'id', 'title', 'total_case', 'create_at', 'update_at', 'create_by',
            'update_by', 'build_cases', 'periodic_expr', 'periodic_switch',
            'env_list', 'region_list', 'project_id', 'project_name', 'branch', 'expect_pass', 'extra_data'
        )
        read_only_fields = ('create_by', 'update_by')

    def validate(self, attrs):
        # validate periodic
        if attrs.get('periodic_switch') and not attrs.get('periodic_expr'):
            raise ValidationException(detail='Params error', code=10110)
        return attrs

    def to_representation(self, instance):
        instance.env_list = id_str_to_set(instance.envs, to_int=True)
        if instance.regions is None:
            instance.region_list = []
        else:
            instance.region_list = id_str_to_set(instance.regions, to_int=True)
        return super().to_representation(instance)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['envs'] = join_id_to_str(ret.pop('env_list'))
        if ret.get('region_list'):
            ret['regions'] = join_id_to_str(ret.pop('region_list'))
        request = self.context.get('request')
        if not request:
            return ret
        if request.method == 'POST':
            ret['create_by'] = request.user.email
        ret['update_by'] = request.user.email
        return ret
