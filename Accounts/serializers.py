from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password',
                  'is_active', 'date_joined')
        extra_kwargs = {
            'password': {'write_only': True,
                         'style': {'input_type': 'password'}},
            'date_joined': {'read_only': True},
            'is_active': {'read_only': True},
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).update(instance, validated_data)
