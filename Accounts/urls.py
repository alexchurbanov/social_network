from django.urls import path
from .views import UsersViewSet, user_activity_view

urlpatterns = [
    path('<uuid:user_id>/activity/', user_activity_view, name='last_activity')
]
