from django_filters import rest_framework as filters
from .models import PostAnalytics, Post


class AnalyticsFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    likes_more_than = filters.Filter(field_name='likes', lookup_expr='gt')
    likes_less_than = filters.Filter(field_name='likes', lookup_expr='lt')

    class Meta:
        model = PostAnalytics
        fields = ('date_from', 'date_to')


class PostsFilter(filters.FilterSet):
    date_published_from = filters.DateTimeFilter(field_name='date_published', lookup_expr='gte')
    date_published_to = filters.DateTimeFilter(field_name='date_published', lookup_expr='lte')
    last_edit_from = filters.DateTimeFilter(field_name='last_edit', lookup_expr='gte')
    last_edit_to = filters.DateTimeFilter(field_name='last_edit', lookup_expr='lte')
    owner_username = filters.Filter(field_name='owner__username')
    liked_by = filters.Filter(field_name='liked_by__username')
    likes_more_than = filters.Filter(field_name='likes', lookup_expr='gt')
    likes_less_than = filters.Filter(field_name='likes', lookup_expr='lt')

    class Meta:
        model = Post
        fields = ('date_published_from', 'date_published_to', 'last_edit_from',
                  'last_edit_to', 'owner_username', 'liked_by', 'likes_more_than',
                  'likes_less_than')
