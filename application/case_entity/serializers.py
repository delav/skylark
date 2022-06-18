from rest_framework import serializers
from application.case_entity.models import CaseEntity


class CaseEntitySerializers(serializers.ModelSerializer):

    class Meta:
        model = CaseEntity
        fields = '__all__'
