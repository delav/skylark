from rest_framework import serializers
from application.userkeyword.models import UserKeyword


class UserKeywordSerializers(serializers.ModelSerializer):

    image = serializers.ImageField(required=False)

    class Meta:
        model = UserKeyword
        fields = '__all__'
        extra_kwargs = {
            'create_at': {'read_only': True},
            'update_at': {'read_only': True},
        }