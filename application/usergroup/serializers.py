from rest_framework import serializers
from application.usergroup.models import Group, UserGroup
from infra.django.exception import ValidationException


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class UserGroupSerializers(serializers.ModelSerializer):

    id = serializers.SerializerMethodField(help_text='group id')
    name = serializers.SerializerMethodField(help_text='group name')

    class Meta:
        model = UserGroup
        fields = ('id', 'name', 'department_id', 'library_path')

    def get_id(self, obj):
        return obj.group.id

    def get_name(self, obj):
        return obj.group.name


class UserGroupAddSerializers(serializers.ModelSerializer):

    name = serializers.CharField(help_text='group name')

    class Meta:
        model = UserGroup
        fields = ('name', 'department_id', 'library_path')

    def validate(self, attrs):
        group_query = Group.objects.filter(name=attrs.get('name'))
        if group_query.exists():
            raise ValidationException(detail='Group name already exist', code=10032)
        return attrs
