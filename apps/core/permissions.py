from rest_framework import permissions
from care_adopt_backend import utils


class OrganizationPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is None:
            return False
        if request.method == "PUT" or request.method == "PATCH":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_employee:
            employee = request.user.employee_profile

            organizations = employee.organizations.all()
            organizations_managed = employee.organizations_managed.all()
            return obj in organizations or obj in organizations_managed

        return False


class FacilityPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is None:
            return False
        if request.method == "POST":
            if employee_profile.organizations_managed.all().count() > 0:
                return True
        if request.method == "PUT" or request.method == "PATCH" or request.method == "DELETE":
            if employee_profile.facilities_managed.all().count() > 0:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is None:
            return False
        if request.method == "PUT" or request.method == "PATCH" or request.method == "DELETE":
            return obj in employee_profile.facilities_managed.all()
        return False

 
class EmployeeProfilePermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is None:
            return False
        if request.method == "POST" or request.method == "DELETE":
            return False
        if request.method == "PUT" or request.method == "PATCH":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        employee_profile = utils.employee_profile_or_none(request.user)
        if employee_profile is None:
            return False
        if employee_profile.organizations_managed.all().count() > 0:
            return True
        return employee_profile == obj
