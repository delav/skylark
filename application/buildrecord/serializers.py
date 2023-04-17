from rest_framework import serializers
from application.buildrecord.models import BuildRecord


class BuildRecordSerializers(serializers.ModelSerializer):
    env_list = serializers.ListField()
    region_list = serializers.ListField(required=False)

    class Meta:
        model = BuildRecord
        fields = '__all__'

    def to_representation(self, instance: BuildRecord):
        instance.env_list = [int(i) for i in instance.envs.split(',')]
        instance.region_list = [int(i) for i in instance.regions.split(',')]
        return super(BuildRecordSerializers, self).to_representation(instance)

    def to_internal_value(self, data):
        ret = super(BuildRecordSerializers, self).to_internal_value(data)
        if ret.get('env_list'):
            ret['envs'] = ','.join(str(i) for i in ret['env_list'])
        if ret.get('region_list'):
            ret['regions'] = ','.join(str(i) for i in ret['region_list'])
        return ret

