from rest_framework import permissions


class IsPatientOrEmployeeForTask(permissions.BasePermission):

    def has_permission(self, request, view):
        SAFE_AND_UPDATE = permissions.SAFE_METHODS + ('PUT', 'PATCH')
        if request.method in SAFE_AND_UPDATE:
            return request.user.is_patient or request.user.is_employee
        else:
            return request.user.is_employee

    def has_object_permission(self, request, view, obj):
        SAFE_AND_UPDATE = permissions.SAFE_METHODS + ('PUT', 'PATCH')
        if request.method in SAFE_AND_UPDATE:
            return request.user.is_patient or request.user.is_employee
        elif request.method in ["POST", "DELETE"]:
            return request.user.is_employee
