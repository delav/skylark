from rest_framework import serializers
from application.caseentity.models import CaseEntity


class CaseEntitySerializers(serializers.ModelSerializer):

    class Meta:
        model = CaseEntity
        fields = ('id', 'input_args', 'output_args', 'keyword_id', 'keyword_type')


class CaseEntityListSerializers(serializers.ModelSerializer):

    case_id = serializers.IntegerField()
    entity_list = CaseEntitySerializers(many=True)

    class Meta:
        model = CaseEntity
        fields = ('case_id', 'entity_list')
