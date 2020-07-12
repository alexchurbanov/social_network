from rest_framework import routers
from django.urls import path, include
from .views import UsersViewSet, user_activity_view

router = routers.DefaultRouter()
router.register('', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('<uuid:user_id>/activity/', user_activity_view, name='last_activity')
]
