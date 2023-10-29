from rest_framework import serializers
from infra.django.exception import ValidationException
from application.buildplan.models import BuildPlan
from infra.utils.typetransform import id_str_to_set, join_id_to_str


class BuildPlanSerializers(serializers.ModelSerializer):
    env_list = serializers.ListField(help_text='env id list')
    region_list = serializers.ListField(required=False, help_text='region id list')
    case_list = serializers.ListField(required=False, help_text='plan case id list')

    class Meta:
        model = BuildPlan
        fields = (
            'id', 'title', 'total_case', 'create_at', 'update_at', 'create_by', 'update_by',
            'periodic_expr', 'periodic_switch', 'env_list', 'region_list', 'case_list', 'auto_latest', 'project_id',
            'branch', 'expect_pass', 'notice_open'
        )
        read_only_fields = ('status', 'create_by', 'update_by')

    def validate(self, attrs):
        # validate periodic
        if attrs.get('periodic_switch') and not attrs.get('periodic_expr'):
            raise ValidationException(detail='Params error', code=10110)
        # validate build case
        if not any([attrs.get('case_list'), attrs.get('auto_latest')]):
            raise ValidationException(detail='Params error', code=10111)
        return attrs

    def to_representation(self, instance):
        instance.env_list = id_str_to_set(instance.envs, to_int=True)
        if not instance.regions:
            instance.region_list = []
        else:
            instance.region_list = id_str_to_set(instance.regions, to_int=True)
        instance.case_list = id_str_to_set(instance.build_cases, to_int=True)
        return super().to_representation(instance)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['envs'] = join_id_to_str(ret.pop('env_list'))
        if ret.get('region_list'):
            ret['regions'] = join_id_to_str(ret.pop('region_list'))
        if ret.get('case_list'):
            ret['total_case'] = len(ret.get('case_list'))
            ret['build_cases'] = join_id_to_str(ret.pop('case_list'))
        request = self.context.get('request')
        if not request:
            return ret
        if request.method == 'POST':
            ret['create_by'] = request.user.email
        ret['update_by'] = request.user.email
        return ret
