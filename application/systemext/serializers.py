from datetime import datetime
from django import forms
from rest_framework import serializers
from application.systemext.models import SystemExt


class SystemExtSerializers(serializers.ModelSerializer):
    expire_at = serializers.CharField(required=False, help_text='expire time str, format: %Y-%m-%d %H:%S:%M')

    class Meta:
        model = SystemExt
        fields = '__all__'

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        if ret.get('expire_at'):
            ret['expire_at'] = datetime.strptime(ret['expire_at'], '%Y-%m-%d %H:%S:%M')
        return ret


class FeedbackForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    info_type = forms.IntegerField(help_text='system info type')
    extra_data = forms.JSONField(help_text='system extra data')
