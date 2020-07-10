from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('auth/jwt/create/', TokenObtainPairView.as_view(), name='get_tokens'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='refresh_tokens'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='verify_tokens'),
    path('users/', include('Accounts.urls')),
    path('posts/', include('Posts.urls')),
]
