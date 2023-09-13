from rest_framework import serializers
from infra.utils.typetransform import id_str_to_set
from application.buildrecord.models import BuildRecord


class BuildRecordSerializers(serializers.ModelSerializer):

    env_list = serializers.ListField(required=False, help_text='env id list')
    region_list = serializers.ListField(required=False, help_text='region id list')

    class Meta:
        model = BuildRecord
        fields = ('id', 'desc', 'create_at', 'create_by', 'finish_at', 'plan_id',
                  'project_id', 'branch', 'env_list', 'region_list', 'periodic', 'status')

    def to_representation(self, instance):
        instance.env_list = id_str_to_set(instance.envs, to_int=True)
        if instance.regions is None:
            instance.region_list = []
        else:
            instance.region_list = id_str_to_set(instance.regions, to_int=True)
        return super().to_representation(instance)

