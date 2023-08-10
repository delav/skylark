from rest_framework import serializers
from application.testsuite.models import TestSuite


class TestSuiteSerializers(serializers.ModelSerializer):
    suite_dir_id = serializers.IntegerField(help_text='suite dir id')

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'document', 'category', 'create_at',
                  'update_at', 'create_by', 'update_by', 'suite_dir_id', 'project_id', 'timeout')
        read_only_fields = ('create_by', 'update_by')

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


class DuplicateTestSuiteSerializers(serializers.ModelSerializer):
    to_project_id = serializers.IntegerField(help_text='to project id')
    to_dir_id = serializers.IntegerField(help_text='to suite dir id')
    raw_suite_id = serializers.IntegerField(help_text='copy test suite id')

    class Meta:
        model = TestSuite
        fields = ('to_project_id', 'to_dir_id', 'raw_suite_id')

