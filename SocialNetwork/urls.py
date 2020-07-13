from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework import routers
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from Accounts.views import JWTObtainPairView, LoginView, logout_view, UsersViewSet
from Posts.views import PostsAnalyticsViewSet, PostViewSet


schema_view = get_schema_view(
    title='Social Network',
    version='v1',
    description='Simple REST API',
)

api_router = routers.DefaultRouter()
api_router.register('analytics', PostsAnalyticsViewSet, basename='analytics')
api_router.register('posts', PostViewSet, basename='posts')
api_router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', logout_view, name='logout'),
    path('api/auth/jwt/create/', JWTObtainPairView.as_view(), name='get_tokens'),
    path('api/auth/jwt/refresh/', TokenRefreshView.as_view(), name='refresh_tokens'),
    path('api/auth/jwt/verify/', TokenVerifyView.as_view(), name='verify_tokens'),
    path('api/', include(api_router.urls)),
    path('api/users/', include('Accounts.urls')),
    path('api/posts/', include('Posts.urls')),
    path('openapi/', schema_view, name='openapi-schema'),
    path('', TemplateView.as_view(
        template_name='swagger.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
]
