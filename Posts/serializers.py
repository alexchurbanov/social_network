from rest_framework import serializers
from .models import Post, PostAnalytics


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CreateOnlyDefault(serializers.CurrentUserDefault()))
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    liked_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class PostAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostAnalytics
        exclude = ('id',)
