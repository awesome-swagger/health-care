from rest_framework import viewsets, permissions

from ..models import BilledActivity
from ..permissions import IsAdminOrEmployeeActivityOwner
from .serializers import BilledActivitySerializer


class BilledActivityViewSet(viewsets.ModelViewSet):
    """
    Viewset for :model:`billings.BilledActivity`
    ========

    create:
        Creates :model:`billings.BilledActivity` object.
        Only admins and employees are allowed to perform this action.

    update:
        Updates :model:`billings.BilledActivity` object.
        Only admins and employee owners are allowed to perform this action.

    partial_update:
        Updates one or more fields of an existing billed activity object.
        Only admins and employee owners are allowed to perform this action.

    retrieve:
        Retrieves a :model:`billings.BilledActivity` instance.
        Admins and employee members will have access to billed activities that
        belong to the care team.

    list:
        Returns list of all :model:`billings.BilledActivity` objects.
        Admins and employee members will have access to billed activities that
        belong to the care team.

    delete:
        Deletes a :model:`billings.BilledActivity` instance.
        Only admins and employee owners are allowed to perform this action.
    """
    serializer_class = BilledActivitySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployeeActivityOwner,
    )
    queryset = BilledActivity.objects.all()

    def get_queryset(self):
        queryset = super(BilledActivityViewSet, self).get_queryset()
        user = self.request.user

        if user.is_superuser:
            pass

        elif user.is_employee:
            employee = user.employee_profile
            queryset = queryset.filter(
                plan__care_team_members__employee_profile=employee
            )

        elif user.is_patient:
            queryset = queryset.filter(
                plan__patient=user.patient_profile
            )

        return queryset
