from rest_framework import serializers
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):

    group_id = serializers.IntegerField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = LibKeyword
        fields = (
            'id', 'name', 'ext_name', 'desc', 'group_id',
            'input_params', 'input_desc', 'output_params', 'output_desc', 'input_type', 'image', 'mark'
        )
