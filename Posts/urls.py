from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet

router = routers.DefaultRouter()
router.register('', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
]
