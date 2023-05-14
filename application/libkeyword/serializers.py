from rest_framework import serializers
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, help_text='keyword icon')

    class Meta:
        model = LibKeyword
        fields = (
            'id', 'name', 'ext_name', 'desc', 'group_id',
            'input_params', 'input_desc', 'output_params', 'output_desc', 'input_type', 'image', 'mark'
        )
