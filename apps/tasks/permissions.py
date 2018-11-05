from rest_framework import permissions


class IsPatientOrEmployeeForTask(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        SAFE_AND_UPDATE = permissions.SAFE_METHODS + ('PUT', 'PATCH')
        if request.method in SAFE_AND_UPDATE:
            return request.user.is_patient or request.user.is_employee
        else:
            return request.user.is_employee

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        SAFE_AND_UPDATE = permissions.SAFE_METHODS + ('PUT', 'PATCH')
        if request.method in SAFE_AND_UPDATE:
            return request.user.is_patient or request.user.is_employee
        elif request.method in ["POST", "DELETE"]:
            return request.user.is_employee


class IsPatientOrEmployeeReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_patient or request.user.is_employee
        else:
            return request.user.is_patient


class IsEmployeeOrPatientReadOnly(permissions.BasePermission):
    """
    Gives access to employees and admins for all requests while restricts
    patients to only be allowed on GET requests.
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return request.user.is_patient or request.user.is_employee
        else:
            return request.user.is_employee
