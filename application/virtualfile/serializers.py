from rest_framework import serializers
from application.virtualfile.models import VirtualFile


class VirtualFileSerializers(serializers.ModelSerializer):

    class Meta:
        model = VirtualFile
        fields = '__all__'
