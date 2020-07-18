from rest_framework.permissions import BasePermission


class IsProfileOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if 'pk' in view.kwargs.keys():
            if view.kwargs['pk'] == request.user.id or view.kwargs['pk'] == 'me':
                return True
            else:
                return False
        else:
            return True
