from rest_framework import serializers
from application.libkeyword.models import LibKeyword


class LibKeywordSerializers(serializers.ModelSerializer):

    group_id = serializers.IntegerField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = LibKeyword
        fields = (
            'id', 'name', 'ext_name', 'desc', 'group_id',
            'input_arg', 'input_desc', 'output_arg', 'output_desc', 'image', 'mark'
        )
