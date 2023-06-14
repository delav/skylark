from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from infra.common import ecb_decrypt
from application.user.models import User
from infra.django.exception import ValidationException


class UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'group_id')


class UserSerializer(TokenObtainPairSerializer, serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, help_text='password')
    email = serializers.EmailField(read_only=True, help_text='user email')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add user extra info
        # token['name'] = user.username
        return token

    def validate(self, attrs):
        try:
            username = attrs['username']
            raw_password = ecb_decrypt(attrs['password'])
            user = User.objects.get(Q(username=username) | Q(email=username))
            assert check_password(raw_password, user.password)
        except (Exception,):
            raise ValidationException(detail='Incorrect username or password', code=10031)
        refresh = self.get_token(user)

        data = {'user': user, 'token': str(refresh.access_token), 'refresh': str(refresh)}
        return data


class RegisterSerializer(serializers.ModelSerializer):

    group_id = serializers.IntegerField(read_only=True, help_text='user group')
    confirm_password = serializers.CharField(allow_blank=False, write_only=True, help_text='confirm password')

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'is_superuser',
                  'is_staff', 'is_active', 'date_joined', 'group_id')
        extra_kwargs = {
            'username': {
                'min_length': 3,
                'max_length': 24,
                'error_messages': {
                    'min_length': 'Only allow usernames of 3-24 characters',
                    'max_length': 'Only allow usernames of 3-24 characters',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 6,
                'max_length': 64,
                'error_messages': {
                    'min_length': 'Only allow usernames of 6-64 password',
                    'max_length': 'Only allow usernames of 6-64 password',
                }
            },
            'email': {
                'max_length': 64,
                'error_messages': {
                    'invalid': 'Invalid email address',
                    'max_length': 'email not allow greater than 64 characters',
                }
            }
        }

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user.exists():
            raise ValidationException(detail='Email has been registered', code=10032)
        return value

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise ValidationException(detail='Username already exists', code=10033)
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationException(detail='Confirm password error', code=10034)
        try:
            raw_password = ecb_decrypt(attrs['password'])
            attrs['password'] = make_password(raw_password)
        except (Exception,):
            raise ValidationException(detail='Please check your password', code=10035)
        del attrs['confirm_password']
        return attrs
