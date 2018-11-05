from rest_framework import permissions
from care_adopt_backend import utils


class PatientProfilePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "POST":
            return False
        if request.method == "PUT" or request.method == "PATCH" or request.method == "DELETE":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        employee_profile = utils.employee_profile_or_none(request.user)
        patient_profile = utils.patient_profile_or_none(request.user)
        if request.method == "PUT" or request.method == "PATCH":
            if employee_profile and obj.facility in employee_profile.facilities_managed.all():
                return True
            if patient_profile and patient_profile == obj:
                return True
        if request.method == "DELETE":
            return employee_profile and obj.facility in employee_profile.facilities_managed.all()
        return False


class PatientSearchPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        # Must be an employee to hit the search endpoint.
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is not None:
            return True
        return False
