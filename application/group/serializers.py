from rest_framework import serializers
from application.infra.exception import ValidationException
from .models import Group


class GroupSerializers(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def validate_name(self, value):
        name_query = Group.objects.filter(name=value)
        if name_query.exists():
            raise ValidationException(detail='group had exists', code=3000010)
        return value
