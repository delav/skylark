from rest_framework import serializers
from application.userkeyword.models import UserKeyword


class UserKeywordSerializers(serializers.ModelSerializer):

    image = serializers.ImageField(required=False, help_text='keyword icon')

    class Meta:
        model = UserKeyword
        fields = '__all__'
