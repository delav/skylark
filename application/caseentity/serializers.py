from rest_framework import serializers
from application.caseentity.models import CaseEntity


class CaseEntitySerializers(serializers.ModelSerializer):

    class Meta:
        model = CaseEntity
        fields = '__all__'
