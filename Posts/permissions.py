from rest_framework.permissions import BasePermission
from django.core.exceptions import ValidationError
from .models import Post


class IsPostOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if 'pk' in view.kwargs.keys():
            if request.user.is_anonymous:
                return False
            try:
                post = Post.objects.get(pk=view.kwargs['pk'])
            except (Post.DoesNotExist, ValidationError):
                return True

            if post.owner == request.user:
                return True
            else:
                return False
        else:
            return True
