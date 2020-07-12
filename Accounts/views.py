from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from .serializers import UserSerializer, JWTObtainPairSerializer, UserLastActivitySerializer, UserLoginSerializer
from .models import User, UserLastActivity
from Accounts.functions import log_user_activity, get_client_ip


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = ''
        user = self.request.user
        if user.is_superuser:
            queryset = User.objects.all().order_by('username')
        elif user.is_authenticated:
            queryset = User.objects.filter(id=user.id)
        return queryset

    def create(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            if not request.user.is_superuser:
                return Response({'status': 'error',
                                 'message': 'you already signed up'})

        return super(UsersViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='delete user')

        return super(UsersViewSet, self).destroy(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get user')

        return super(UsersViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get user')

        return super(UsersViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='edit user')

        return super(UsersViewSet, self).update(request, *args, **kwargs)


class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTObtainPairSerializer


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def user_activity_view(request, user_id):
    if not request.user.is_superuser:
        if request.user.id != user_id:
            return Response({'status': 'error'}, status=status.HTTP_401_UNAUTHORIZED)

    instance = UserLastActivity.objects.get(user=user_id)
    serializer = UserLastActivitySerializer(instance)
    return Response(serializer.data)


class LoginView(GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        email = request.data['email']
        password = request.data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'status': 'success',
                             'message': 'logged in'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error',
                             'message': 'wrong email or password'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def logout_view(request):
    logout(request)
    return Response({'status': 'success',
                     'message': 'logged out'}, status=status.HTTP_200_OK)
