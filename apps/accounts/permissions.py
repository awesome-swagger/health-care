from rest_framework import permissions
from rest_framework.permissions import BasePermission


class BaseUserPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.is_authenticated() or request.method == 'POST'

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method not in permissions.SAFE_METHODS:
            return obj.id == request.user.id
        else:
            return True
