from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from .models import User


class UsersViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = ''
        user = self.request.user
        if user.is_superuser or user.is_staff:
            queryset = User.objects.all().order_by('username')
        elif user.is_authenticated:
            queryset = User.objects.filter(id=user.id)
        return queryset
