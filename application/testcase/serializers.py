from rest_framework import serializers
from application.testcase.models import TestCase


class TestCaseSerializers(serializers.ModelSerializer):
    priority_id = serializers.IntegerField(required=False)
    test_suite_id = serializers.IntegerField()
    create_by = serializers.CharField(source='create_by.email')
    update_by = serializers.CharField(source='update_by.email')

    class Meta:
        model = TestCase
        fields = (
            'id', 'name', 'category', 'document', 'priority_id',
            'create_at', 'update_at', 'create_by', 'update_by', 'test_suite_id', 'inputs', 'outputs', 'timeout'
        )

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user
        attrs['update_by'] = request.user
        return attrs
