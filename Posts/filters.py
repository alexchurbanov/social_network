from django_filters import rest_framework as filters
from rest_framework.filters import BaseFilterBackend

from .models import Post


class PostsFilter(filters.FilterSet):
    date_published_from = filters.DateTimeFilter(field_name='date_published', lookup_expr='gte')
    date_published_to = filters.DateTimeFilter(field_name='date_published', lookup_expr='lte')
    author_username = filters.Filter(field_name='author__username')
    liked_by = filters.Filter(field_name='liked_by__username')

    class Meta:
        model = Post
        fields = ('date_published_from', 'date_published_to', 'author_username', 'liked_by')


class DateRangePostLikesFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)
        if date_from and date_to:
            queryset = queryset.filter(created__gte=date_from,
                                       created__lte=date_to)
        elif date_from:
            queryset = queryset.filter(created__gte=date_from)
        elif date_to:
            queryset = queryset.filter(created__lte=date_to)

        return queryset
