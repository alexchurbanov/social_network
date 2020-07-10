from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
