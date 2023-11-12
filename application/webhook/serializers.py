from rest_framework import serializers
from application.webhook.models import Webhook


class WebhookSerializers(serializers.ModelSerializer):

    class Meta:
        model = Webhook
        fields = '__all__'
