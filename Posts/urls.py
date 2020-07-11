from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet, like_post, unlike_post, PostAnalyticsViewSet

router = routers.DefaultRouter()
router.register('list', PostViewSet, basename='posts')
router.register('analytics', PostAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('list/<str:post_id>/like/', like_post, name='like_post'),
    path('list/<str:post_id>/unlike/', unlike_post, name='unlike_post'),
]
