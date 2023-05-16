from rest_framework import serializers
from application.buildrecord.models import BuildRecord
from application.infra.utils.typetransform import id_str_to_set, join_id_to_str


class BuildRecordSerializers(serializers.ModelSerializer):
    env_list = serializers.ListField(help_text='env id list')
    region_list = serializers.ListField(required=False, help_text='region id list')

    class Meta:
        model = BuildRecord
        fields = '__all__'

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
        request = self.context.get('request')
        if not request:
            return ret
        if request.method == 'POST':
            ret['create_by'] = request.user.email
        return ret

