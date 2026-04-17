from rest_framework import permissions

class IsDoctor(permissions.BasePermission):
    """
    Allows access only to doctor (physician) users.
    """
    message = "You do not have permission to perform this action. Doctors only."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'physician')
