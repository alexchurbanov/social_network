from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework as filters

from .serializers import (UserSerializer, JWTObtainPairSerializer,
                          UserLastActivitySerializer, UserLoginSerializer,
                          UserDetailSerializer, ChangePasswordSerializer)
from .models import User, UserLastActivity
from Accounts.functions import log_user_activity, get_client_ip
from .filters import UsersFilter
from .permissions import IsProfileOwnerOrAdmin


class UsersViewSet(viewsets.ModelViewSet):
    """
    List of active users
    """
    serializer_class = UserSerializer
    detail_serializer_class = UserDetailSerializer
    change_password_serializer_class = ChangePasswordSerializer
    permission_classes = (AllowAny, IsProfileOwnerOrAdmin)

    filter_backends = (filters.DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering_fields = ('date_joined', 'username')
    filterset_class = UsersFilter

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by('username')

    def get_object(self):
        if self.kwargs['pk'] == 'me':
            return self.request.user
        else:
            return super().get_object()

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        if self.action == 'change_password':
            return self.change_password_serializer_class(*args, **kwargs)
        elif self.action == 'update':
            return self.detail_serializer_class(*args, **kwargs)
        else:
            return self.serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return Response({'status': 'error',
                             'message': 'you already signed up'})

        return super(UsersViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Set none active status to your account
        """
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='delete user')
        if kwargs['pk'] == request.user.id or kwargs['pk'] == 'me' or request.user.is_superuser:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            return Response({'status': 'success',
                             'message': 'Account is not active now'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error',
                             'message': "You don't have permissions to do that"}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get users')

        return super(UsersViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        If provided 'id' is "me" then return the current user.
        """
        if not request.user.is_authenticated:
            return Response({'status': 'error',
                             'message': 'Log in first'}, status=status.HTTP_401_UNAUTHORIZED)

        if kwargs['pk'] == 'me':
            serializer = self.detail_serializer_class
        else:
            serializer = self.get_serializer

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get user')
        instance = self.get_object()
        serialized = serializer(instance)
        return Response(serialized.data)

    @action(methods=['POST'], detail=True, serializer_class=ChangePasswordSerializer)
    def change_password(self, request, pk):
        """
        Change your password.
        """
        if pk != 'me' and pk != request.user.id:
            return Response({'status': 'error',
                             'message': 'You can change only your password'}, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not instance.check_password(request.data['old_password']):
                return Response({'old_password': ['Wrong password.']}, status=status.HTTP_400_BAD_REQUEST)
            instance.set_password(request.data['new_password'])
            instance.save()

            log_user_activity(request.user, last_request_IP=get_client_ip(request),
                              last_request=timezone.now(), last_request_type='password change')

            return Response({'status': 'success',
                             'message': 'Password updated successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True)
    def activity(self, request, pk):
        """
        Shows when user was logged in last time and when he made last
        request to the service.
        """
        if not request.user.is_authenticated:
            return Response({'status': 'error',
                             'message': 'Log in first'}, status=status.HTTP_401_UNAUTHORIZED)
        if pk == 'me':
            pk = request.user.id
        else:
            if request.user.id != pk:
                if not request.user.is_superuser or not request.user.is_staff:
                    return Response({'status': 'error',
                                     'message': 'Unauthorized to see this user activity'},
                                    status=status.HTTP_401_UNAUTHORIZED)

        try:
            instance = UserLastActivity.objects.get(user=pk)
            serializer = UserLastActivitySerializer(instance)
        except UserLastActivity.DoesNotExist:
            return Response({'status': 'error',
                             'message': "User with this id doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        log_user_activity(request.user, last_request_IP=get_client_ip(request),
                          last_request=timezone.now(), last_request_type='get user activity')

        return Response(serializer.data)


class JWTObtainPairView(TokenObtainPairView):
    """
    JWT login. Take user credentials and return refresh and access JWT
    """
    serializer_class = JWTObtainPairSerializer


class LoginView(GenericAPIView):
    """
    Session login.
    """
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):

        email = request.data['email']
        password = request.data['password']

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    """
    Logout for authenticated users that using session.
    """
    logout(request)
    return Response({'status': 'success',
                     'message': 'logged out'}, status=status.HTTP_200_OK)
