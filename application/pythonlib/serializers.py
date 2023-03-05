from rest_framework import serializers
from application.pythonlib.models import PythonLib


class PythonLibSerializers(serializers.ModelSerializer):

    class Meta:
        model = PythonLib
        fields = '__all__'
