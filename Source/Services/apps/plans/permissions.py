from care_adopt_backend.permissions import IsAdminOrEmployee


class CareTeamMemberPermissions(IsAdminOrEmployee):

    def has_object_permission(self, request, view, obj):

        if request.method == 'DELETE':
            if request.user.is_superuser:
                return True

            if request.user.is_employee:
                employee = request.user.employee_profile
                manager_role = employee.assigned_roles.filter(is_manager=True)
                if manager_role.exists():
                    return True

        return True
