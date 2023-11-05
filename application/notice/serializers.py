from rest_framework import serializers
from application.notice.models import Notice


class NoticeSerializers(serializers.ModelSerializer):
    rcv_email = serializers.ListField(help_text='email list')

    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ('create_by', 'update_by')

    def to_representation(self, instance):
        emails = instance.rcv_email
        if emails:
            instance.rcv_email = emails.split(',')
        return super().to_representation(instance)

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        ret['rcv_email'] = ','.join(ret['rcv_email'])
        request = self.context.get('request')
        if request.method == 'POST':
            ret['create_by'] = request.user.email
        ret['update_by'] = request.user.email
        return ret
