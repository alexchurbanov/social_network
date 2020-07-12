from rest_framework import routers
from django.urls import path, include
from .views import PostViewSet, like_post, unlike_post, PostsAnalyticsViewSet

router = routers.DefaultRouter()
router.register('list', PostViewSet, basename='posts')
router.register('analytics', PostsAnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('list/<uuid:post_id>/like/', like_post, name='like_post'),
    path('list/<uuid:post_id>/unlike/', unlike_post, name='unlike_post'),
]
