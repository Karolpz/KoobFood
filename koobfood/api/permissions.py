from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsManagerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.restaurant.manager == request.user
    
class IsManagerOrReadOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.groups.filter(name='Manager').exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.manager == request.user

class IsOwnerOrManagerReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):  
        if request.method in permissions.SAFE_METHODS:
            return obj.customer == request.user or obj.restaurant.manager == request.user
        return obj.customer == request.user
        