from rest_framework import serializers
from application.notice.models import Notice
from infra.utils.typetransform import id_str_to_set, join_id_to_str


class NoticeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = '__all__'

    def to_representation(self, instance):
        emails = instance.rcv_email
        if emails:
            instance.rcv_email = emails.split(',')
        return super().to_representation(instance)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['rcv_email'] = ','.join(ret['rcv_email'])
        request = self.context.get('request')
        if not request:
            return ret
        if request.method == 'POST':
            ret['create_by'] = request.user.email
        ret['update_by'] = request.user.email
        return ret
