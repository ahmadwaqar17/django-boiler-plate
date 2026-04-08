from rest_framework import permissions

class IsTechnician(permissions.BasePermission):
    """
    Allows access only to technician users.
    """
    message = "You do not have permission to perform this action. Technicians only."

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'technician')
