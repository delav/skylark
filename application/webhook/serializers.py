from django.conf import settings
from rest_framework import serializers
from application.webhook.models import Webhook


class WebhookSerializers(serializers.ModelSerializer):
    payload_url = serializers.SerializerMethodField('get_payload_url')

    class Meta:
        model = Webhook
        fields = (
            'id', 'name', 'hook_type', 'payload_url', 'create_at',
            'update_at', 'create_by', 'update_by', 'status', 'desc', 'extra_data'
        )
        read_only_fields = ('create_by', 'update_by')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret

    def get_payload_url(self, obj):
        return settings.SERVER_DOMAIN + '/webhook?secret=' + obj.secret
