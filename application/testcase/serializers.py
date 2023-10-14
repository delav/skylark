from rest_framework import serializers
from application.testcase.models import TestCase


class TestCaseSerializers(serializers.ModelSerializer):
    test_suite_id = serializers.IntegerField(help_text='test suite id')

    class Meta:
        model = TestCase
        fields = (
            'id', 'name', 'category', 'document', 'priority_id', 'create_at', 'update_at',
            'create_by', 'update_by', 'test_suite_id', 'order', 'project_id', 'inputs', 'outputs', 'timeout', 'status'
        )
        read_only_fields = ('category', 'status')

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        request = self.context.get('request')
        if not request:
            return ret
        user_email = request.user.email
        if request.method == 'POST':
            ret['create_by'] = user_email
        ret['update_by'] = user_email
        return ret

    def validate(self, attrs):
        request = self.context.get('request')
        if request.method == 'PUT':
            # not allowed update project id
            del attrs['project_id']
        return attrs


class DuplicateTestCaseSerializers(serializers.ModelSerializer):
    to_project_id = serializers.IntegerField(help_text='to project id')
    to_suite_id = serializers.IntegerField(help_text='to test suite id')
    raw_case_id = serializers.IntegerField(help_text='copy test case id')

    class Meta:
        model = TestCase
        fields = ('to_project_id', 'to_suite_id', 'raw_case_id')
