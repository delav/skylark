from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password, check_password
from application.utils.common.crypter import ecb_decrypt
from application.user.models import User
from application import ValidationException


class LoginSerializer(TokenObtainPairSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    @classmethod
    def get_token(cls, user):
        """
        此方法往token的有效负载 payload 里面添加数据
        例如自定义了用户表结构，可以在这里面添加用户邮箱，头像图片地址，性别，年龄等可以公开的信息
        这部分放在token里面是可以被解析的，所以不要放比较私密的信息

        :param user: 用戶信息
        :return: token
        """
        token = super().get_token(user)
        # 添加个人信息
        # token['name'] = user.username
        return token

    def validate(self, attrs):
        try:
            raw_password = ecb_decrypt(attrs['password'])
            user = User.objects.get(username=attrs['username'])
            assert check_password(raw_password, user.password)
        except (Exception,):
            raise ValidationException(detail='用户名或密码错误', code=3000030)
        refresh = self.get_token(user)

        data = {'user': user, 'token': str(refresh.access_token), 'refresh': str(refresh)}
        return data


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(label='确认密码', help_text='确认密码',
                                             min_length=6, max_length=64,
                                             write_only=True,
                                             error_messages={
                                                 'min_length': '仅允许6~64个字符的确认密码',
                                                 'max_length': '仅允许6~64个字符的确认密码',
                                             })
    group_id = serializers.IntegerField(required=False, read_only=True, help_text='所属组ID')

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password', 'first_name', 'last_name', 'email', 'is_superuser',
                  'is_staff', 'is_active', 'date_joined', 'group_id')
        extra_kwargs = {
            'username': {
                'label': '用户名',
                'help_text': '用户名',
                'min_length': 3,
                'max_length': 24,
                'error_messages': {
                    'min_length': '仅允许3-24个字符的用户名',
                    'max_length': '仅允许3-24个字符的用户名',
                }
            },
            'password': {
                'label': '密码',
                'help_text': '密码',
                'write_only': True,
                'min_length': 6,
                'max_length': 64,
                'error_messages': {
                    'min_length': '仅允许6-64个字符的密码',
                    'max_length': '仅允许6-64个字符的密码',
                }
            },
            'email': {
                'label': '邮箱',
                'help_text': '邮箱',
                'max_length': 64,
                'error_messages': {
                    'invalid': '邮箱地址不合法',
                    'max_length': '不能大于64个字符的邮箱',
                }
            }
        }

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user.exists():
            raise ValidationException(detail='邮箱已注册', code=3000021)
        return value

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user.exists():
            raise ValidationException(detail='用户名已注册', code=3000022)
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ValidationException(detail='密码与确认密码不一致', code=3000020)
        try:
            raw_password = ecb_decrypt(attrs['password'])
            attrs['password'] = make_password(raw_password)
        except (Exception,):
            raise ValidationException(detail='密码不合法', code=3000023)
        del attrs['confirm_password']
        return attrs
