from rest_framework import serializers
from application.group.models import Group


class GroupSerializers(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

