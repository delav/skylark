from rest_framework import serializers
from application.casetag.models import CaseTag


class CaseTagSerializers(serializers.ModelSerializer):
    project_id = serializers.IntegerField(required=False)

    class Meta:
        model = CaseTag
        fields = ('id', 'tag_name', 'project_id')