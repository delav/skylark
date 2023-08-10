from rest_framework import serializers
from application.department.models import Department


class DepartmentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = '__all__'
