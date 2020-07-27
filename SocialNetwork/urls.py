from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from Accounts.views import UsersViewSet
from Posts.views import PostViewSet, posts_analytics_view


schema_view = get_schema_view(
    title='Social Network',
    version='v1',
    description='Django REST API for social network',
)

api_router = routers.DefaultRouter()
api_router.register('posts', PostViewSet, basename='posts')
api_router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(api_router.urls)),
    path('api/v1/auth/', include('Accounts.urls')),
    path('api/v1/analytics/', posts_analytics_view, name='analytics'),
    path('openapi/', schema_view, name='openapi-schema'),
    path('', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
