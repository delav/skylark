from rest_framework import serializers
from application.testsuite.models import TestSuite


class TestSuiteSerializers(serializers.ModelSerializer):

    suite_dir_id = serializers.IntegerField()
    create_by = serializers.CharField(source='create_by.email')
    update_by = serializers.CharField(source='update_by.email')

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'document', 'category', 'create_at',
                  'update_at', 'create_by', 'update_by', 'suite_dir_id', 'timeout')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user
        attrs['update_by'] = request.user
        return attrs
