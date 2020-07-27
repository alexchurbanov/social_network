from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer, PasswordField,
                                                  TokenRefreshSerializer)
from django.contrib.auth.signals import user_logged_in
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


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
        fields = ('id', 'username', 'is_staff',
                  'date_joined', 'email')
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
        model = User
        fields = ('last_login', 'last_request', 'last_IP')


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        access = refresh.access_token

        data['refresh'] = str(refresh)
        data['access'] = str(access)
        data['exp_date'] = {
                               'refresh': refresh['exp'],
                               'access': access['exp']
        }
        data['user'] = self.user.username

        user_logged_in.send(self.user.__class__, user=self.user, request=self.context['request'])
        return data


class JWTRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        access = refresh.access_token

        data = {'access': str(access), 'exp_date': {}}
        data['exp_date']['access'] = access['exp']

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = str(refresh)
            data['exp_date']['refresh'] = refresh['exp']

        return data
