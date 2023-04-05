from rest_framework import serializers
from application.testsuite.models import TestSuite


class TestSuiteSerializers(serializers.ModelSerializer):

    suite_dir_id = serializers.IntegerField()
    create_by = serializers.CharField(read_only=True)
    update_by = serializers.CharField(read_only=True)

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'document', 'category', 'create_at',
                  'update_at', 'create_by', 'update_by', 'suite_dir_id', 'timeout')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            attrs['create_by'] = request.user.email
        attrs['update_by'] = request.user.email
        return attrs
