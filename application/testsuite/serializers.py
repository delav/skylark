from rest_framework import serializers
from application.testsuite.models import TestSuite
from application.tag.serializers import TagSerializers


class TestSuiteSerializers(serializers.ModelSerializer):

    suite_dir_id = serializers.IntegerField()
    tags = TagSerializers(many=True, required=False)

    class Meta:
        model = TestSuite
        fields = ('id', 'name', 'category', 'tags', 'suite_dir_id', 'timeout')