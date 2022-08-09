from rest_framework import serializers
from application.testcase.models import TestCase
from application.casetag.serializers import CaseTagSerializers


class TestCaseSerializers(serializers.ModelSerializer):
    case_pri_id = serializers.IntegerField()
    test_suite_id = serializers.IntegerField()
    case_tag = CaseTagSerializers(many=True, required=False)

    class Meta:
        model = TestCase
        fields = ('id', 'case_name', 'case_desc', 'case_pri_id',
                  'case_tag', 'test_suite_id', 'case_type', 'inputs', 'outputs', 'timeout')
