from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsAdminUser(BasePermission):
    """
    Custom permission to only allow access to admin users.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and is an admin
        if request.user and request.user.is_authenticated:
            if not request.user.is_admin:
                raise PermissionDenied(detail="You need admin privileges to access this resource.")
            return True
        raise PermissionDenied(detail="Authentication required to access this resource.")