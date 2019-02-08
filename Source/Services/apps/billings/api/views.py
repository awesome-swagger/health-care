import datetime

from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin

from ..models import BilledActivity
from ..permissions import IsAdminOrEmployeeActivityOwner
from .serializers import BilledActivitySerializer
from apps.core.api.mixins import ParentViewSetPermissionMixin
from apps.core.api.views import OrganizationViewSet
from apps.core.models import Organization
from apps.patients.models import PatientProfile


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
        spent_time = BilledActivity().total_spent_time(user.employee_profile) if user.is_employee else 0
        return Response(
            {"total_tracked_time": spent_time}
        )


class OrganizationBilledActivity(ParentViewSetPermissionMixin,
                                 NestedViewSetMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    """

    list:
        Returns list of all :model:`billings.BilledActivity` objects related
        to the parent organization.
        Admins and employee members will have access to billed activities that
        belong to the care team.


    Filtering
    ---
    This endpoint also allows users to filter by `facility` and
    `service area`. Please see the examples below:

        - GET /api/organizations/<organization-ID>/billed_activities/?plan__patient__facility=<facility-ID>
        - GET /api/organizations/<organization-ID>/billed_activities/?plan_template__service_area=<service-area-ID>
        - GET /api/organizations/<organization-ID>/billed_activities/?plan__patient__facility=<facility-ID>&plan_template__service_area=<service-area-ID>


    """

    serializer_class = BilledActivitySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsAdminOrEmployeeActivityOwner,
    )
    queryset = BilledActivity.objects.all()
    parent_lookup = [
        (
            'plan__patient__facility__organization',
            Organization,
            OrganizationViewSet
        )
    ]
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = (
        'plan__patient__facility',
        'plan_template__service_area',
    )

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

    def _get_billable_patients(self, queryset):
        parents_query_dict = self.get_parents_query_dict()
        organization_id = parents_query_dict['plan__patient__facility__organization']

        return queryset.filter(
            payer_reimbursement=True,
            facility__organization__id=organization_id)

    def get_billable_patients_count(self, queryset):
        patients = self._get_billable_patients(queryset)
        return patients.count()

    def get_total_facilities(self, queryset):
        patients = self._get_billable_patients(queryset)
        return patients.values_list('facility', flat=True).distinct().count()

    @action(methods=['get'], detail=False)
    def overview(self, request, *args, **kwargs):
        """
        This endpoint will return aggregated data for an organization's billings.
        Aggregated data are as follows:

            - billable patients
            - total facilities
            - total practitioners
            - total hours
            - total billable

        Filtering
        ---
        This endpoint also allows users to filter by `facility` and
        `service area`. Please see the examples below:

            - GET /api/organizations/<organization-ID>/billed_activities/overview/?plan__patient__facility=<facility-ID>
            - GET /api/organizations/<organization-ID>/billed_activities/overview/?plan_template__service_area=<service-area-ID>
            - GET /api/organizations/<organization-ID>/billed_activities/overview/?plan__patient__facility=<facility-ID>&plan_template__service_area=<service-area-ID>

        Page Usage
        ---
        - this endpoint will be used in `billing` page

        """
        base_queryset = self.get_queryset()
        queryset = self.filter_queryset(base_queryset)

        # TODO: Add this when the model is ready
        total_practitioners = 0
        total_billable = 0

        time_spent = queryset.aggregate(total=Sum('time_spent'))
        total_time_spent = time_spent['total'] or 0
        total_hours = str(datetime.timedelta(minutes=total_time_spent))[:-3]

        data = {
            'billable_patients': self.get_billable_patients_count(queryset),
            'total_facilities': self.get_total_facilities(queryset),
            'total_practitioners': total_practitioners,
            'total_hours': total_hours,
            'total_billable': total_billable
        }
        return Response(data=data)
