from rest_framework import serializers
from application.infra.django.exception import ValidationException
from application.buildplan.models import BuildPlan
from application.infra.utils.transform import id_str_to_set, join_id_to_str


class BuildPlanSerializers(serializers.ModelSerializer):
    extra_data = serializers.JSONField(required=False)
    env_list = serializers.ListField()
    region_list = serializers.ListField(required=False)

    class Meta:
        model = BuildPlan
        exclude = ('periodic_task_id', )
        read_only_fields = ('create_by', 'update_by')

    def validate(self, attrs):
        # validate periodic
        if attrs.get('periodic_switch') and not attrs.get('periodic_expr'):
            raise ValidationException(detail='Params error', code=10110)
        return attrs

    def to_representation(self, instance):
        instance.env_list = list(id_str_to_set(instance.envs))
        if instance.regions is None:
            instance.region_list = []
        else:
            instance.region_list = list(id_str_to_set(instance.regions))
        return super().to_representation(instance)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['envs'] = join_id_to_str(ret.pop('env_list'))
        if ret.get('region_list'):
            ret['regions'] = join_id_to_str(ret.pop('region_list'))
        request = self.context['request']
        if request.method == 'POST':
            ret['create_by'] = request.user.email
        ret['update_by'] = request.user.email
        return ret
