from rest_framework import serializers
from application.testcase.models import TestCase


class TestCaseSerializers(serializers.ModelSerializer):
    test_suite_id = serializers.IntegerField()

    class Meta:
        model = TestCase
        fields = (
            'id', 'name', 'category', 'document', 'priority_id',
            'create_at', 'update_at', 'create_by', 'update_by', 'test_suite_id', 'inputs', 'outputs', 'timeout'
        )
        read_only_fields = ('create_by', 'update_by')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        return attrs
