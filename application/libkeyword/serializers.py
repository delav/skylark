from rest_framework import serializers
from application.status import KeywordCategory, ModuleStatus
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, help_text='keyword icon')

    class Meta:
        model = LibKeyword
        exclude = ('create_at', 'update_at')

    def validate(self, attrs):
        attrs['category'] = KeywordCategory.CUSTOMIZED
        request = self.context.get('request')
        if request.method == 'POST':
            # new keyword status
            attrs['status'] = ModuleStatus.NORMAL
        return attrs
