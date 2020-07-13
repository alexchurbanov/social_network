from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,PasswordField
from django.contrib.auth.signals import user_logged_in

from .models import User, UserLastActivity


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}},
            'date_joined': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

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


