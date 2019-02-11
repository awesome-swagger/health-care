import datetime

from django.utils.translation import ugettext_lazy as _

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(methods=['post'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def track_time(self, request, *args, **kwargs):
        serializer = BilledActivitySerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        pre_activity = BilledActivity.objects.filter(plan_id=serializer.validated_data.get('plan'),
                                                     activity_type=serializer.validated_data.get('activity_type'),
                                                     added_by_id=serializer.validated_data.get('added_by'),
                                                     activity_date=datetime.date.today()) \
                                             .first()
        if pre_activity:
            pre_activity.time_spent = pre_activity.time_spent + serializer.validated_data.get('time_spent')
            pre_activity.save()
        else:
            serializer.save()

        return Response(
            {"detail": _("Successfully created a billed activity for the plan.")}
        )

    @action(methods=['get'], detail=False,
            permission_classes=(permissions.IsAuthenticated, ))
    def total_tracked_time(self, request, *args, **kwargs):
        user = request.user
        spent_time = user.employee_profile.billable_hours if user.is_employee else 0

        return Response(
            {"total_tracked_time": spent_time}
        )
