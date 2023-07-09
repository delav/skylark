from rest_framework import serializers
from application.usergroup.models import UserGroup


class UserGroupSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserGroup
        fields = '__all__'

