from django_filters import rest_framework as filters
from .models import Post


class PostsFilter(filters.FilterSet):
    date_published_from = filters.DateTimeFilter(field_name='date_published', lookup_expr='gte')
    date_published_to = filters.DateTimeFilter(field_name='date_published', lookup_expr='lte')
    owner_username = filters.Filter(field_name='owner__username')
    liked_by = filters.Filter(field_name='liked_by__username')

    class Meta:
        model = Post
        fields = ('date_published_from', 'date_published_to', 'owner_username', 'liked_by')
