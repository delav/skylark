from rest_framework import serializers
from application.usergroup.models import Group, UserGroup


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class UserGroupSerializers(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'department_id', 'library_path')

    def get_id(self, obj):
        return obj.group.id

    def get_name(self, obj):
        return obj.group.name
