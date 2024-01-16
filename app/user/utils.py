from rest_framework import permissions


from user.models import User

def is_admin_user(user: User) -> bool:
    """
    Check an authenticated user is an admin or not
    """
    return user.is_admin

class IsAdmin(permissions.BasePermission):
    """Allows access only to Admin users."""
    message = "Only Admins are authorized to perform this action."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return is_admin_user(request.user)
