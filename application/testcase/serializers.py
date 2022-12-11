from rest_framework import serializers
from application.testcase.models import TestCase
from application.casetag.serializers import CaseTagSerializers


class TestCaseSerializers(serializers.ModelSerializer):
    priority_id = serializers.IntegerField(required=False)
    test_suite_id = serializers.IntegerField()
    tags = CaseTagSerializers(many=True, required=False)
    update_by = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TestCase
        fields = ('id', 'name', 'category', 'desc', 'priority_id', 'update_by',
                  'tags', 'test_suite_id', 'inputs', 'outputs', 'timeout')
