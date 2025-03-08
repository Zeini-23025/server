from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin'


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, 'role', None) == 'standard'


class IsAuthenticatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsGuest(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


