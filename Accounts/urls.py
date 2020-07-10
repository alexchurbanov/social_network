from rest_framework import routers
from django.urls import path, include
from .views import UsersViewSet

router = routers.DefaultRouter()
router.register('', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
