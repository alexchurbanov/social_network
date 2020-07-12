from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from Accounts.views import JWTObtainPairView, LoginView, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/jwt/create/', JWTObtainPairView.as_view(), name='get_tokens'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='refresh_tokens'),
    path('auth/jwt/verify/', TokenVerifyView.as_view(), name='verify_tokens'),
    path('users/', include('Accounts.urls')),
    path('posts/', include('Posts.urls')),
]
