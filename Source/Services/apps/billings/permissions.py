from care_adopt_backend.permissions import IsAdminOrEmployee


class IsAdminOrEmployeeActivityOwner(IsAdminOrEmployee):

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Only the owner can update/delete an object
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.is_employee and \
                obj.added_by == request.user.employee_profile

        members = obj.team_template.plan.care_team_members.values_list(
            'employee_profile', flat=True).distinct()
        return request.user.is_employee and \
            request.user.employee_profile.id in members
