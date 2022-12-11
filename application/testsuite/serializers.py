from rest_framework import serializers
from application.testsuite.models import TestSuite


class TestSuiteSerializers(serializers.ModelSerializer):

    suite_dir_id = serializers.IntegerField()

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'category', 'suite_dir_id', 'timeout')