from rest_framework import serializers
from application.caseentity.models import CaseEntity


class CaseEntitySerializers(serializers.ModelSerializer):

    class Meta:
        model = CaseEntity
        fields = ('id', 'input_parm', 'output_parm', 'seq_number', 'keyword_id', 'keyword_type')


class CaseEntityListSerializers(serializers.ModelSerializer):

    case_id = serializers.IntegerField(required=True, write_only=True)
    entity_list = CaseEntitySerializers(many=True)

