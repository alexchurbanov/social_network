from rest_framework.permissions import BasePermission


class IsProfileOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.user.is_staff:
            return True

        if 'pk' in view.kwargs.keys():
<<<<<<< Updated upstream
            if view.kwargs['pk'] == 'me':
=======
            if request.user.is_anonymous:
                return False
            if view.kwargs['pk'] == str(request.user.id) or view.kwargs['pk'] == 'me':
>>>>>>> Stashed changes
                return True
            else:
                return False
        else:
            return True
