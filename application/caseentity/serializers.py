from rest_framework import serializers
from application.caseentity.models import CaseEntity
from application.caseentity.handler import get_input_list


class CaseEntitySerializers(serializers.ModelSerializer):

    # input_list = serializers.ListField(help_text='entity input list')
    # output_list = serializers.ListField(help_text='entity output list')

    class Meta:
        model = CaseEntity
        fields = (
            'id', 'input_args', 'output_args', 'keyword_id', 'keyword_type'
        )

    # def to_representation(self, instance):
    #     instance.input_list = get_input_list(instance.keyword_id, instance.keyword_type, instance.input_args)
    #     instance.output_list = get_input_list(instance.keyword_id, instance.keyword_type, instance.output_args)
    #     return super().to_representation(instance)


class CaseEntityListSerializers(serializers.ModelSerializer):

    case_id = serializers.IntegerField(help_text='associated case id')
    entity_list = CaseEntitySerializers(many=True, help_text='case entity list')

    class Meta:
        model = CaseEntity
        fields = (
            'case_id', 'entity_list'
        )
