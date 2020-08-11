from django.urls import path
from .views import LoginView, logout_view, JWTRefreshView, JWTObtainPairView, JWTVerifyView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('jwt/create/', JWTObtainPairView.as_view(), name='get_tokens'),
    path('jwt/refresh/', JWTRefreshView.as_view(), name='refresh_token'),
    path('jwt/verify/', JWTVerifyView.as_view(), name='verify_token'),
]
