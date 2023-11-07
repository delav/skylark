from rest_framework import serializers
from application.status import KeywordCategory, ModuleStatus
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, help_text='keyword icon')

    class Meta:
        model = LibKeyword
        fields = '__all__'
        read_only_fields = ('create_by', 'update_by')

    def validate(self, attrs):
        attrs['category'] = KeywordCategory.CUSTOMIZED
        request = self.context.get('request')
        if request.method == 'POST':
            # new keyword status
            attrs['status'] = ModuleStatus.NORMAL
        return attrs

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret
