from rest_framework import permissions
from care_adopt_backend import utils


class EmployeeOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        employee_profile = utils.employee_profile_or_none(request.user)
        patient_profile = utils.patient_profile_or_none(request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if employee_profile is not None:
                return True
            return False


class IsPatientOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_patient


class IsEmployeeOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_employee


class IsAdminOrEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and \
            (request.user.is_superuser or request.user.is_employee)
