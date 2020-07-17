from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from django.contrib.auth.signals import user_logged_in

from .models import User, UserLastActivity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username',
                  'password', 'date_joined', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}},
            'email': {'write_only': True},
            'date_joined': {'read_only': True},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_superuser', 'is_active',
                   'groups', 'user_permissions',)
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'is_staff': {'read_only': True},
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    class Meta:
        model = User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User


class UserLastActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLastActivity
        exclude = ('id', 'user')


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(JWTObtainPairSerializer, self).validate(attrs)
        user_logged_in.send(self.user.__class__, user=self.user, request=self.context['request'])
        return data
