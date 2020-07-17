from django_filters import rest_framework as filters
from .models import User


class UsersFilter(filters.FilterSet):
    date_joined_from = filters.DateTimeFilter(field_name='date_joined', lookup_expr='gte')
    date_joined_to = filters.DateTimeFilter(field_name='date_joined', lookup_expr='lte')

    class Meta:
        model = User
        fields = ('date_joined_from', 'date_joined_to')
