from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from ..models import BilledActivity, BillingType
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import BasicEmployeeProfileSerializer
from apps.plans.api.serializers import CarePlanSerializer
from apps.tasks.api.serializers import TeamTaskTemplateSerializer
from apps.tasks.models import TeamTask


class BillingTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BillingType
        fields = (
            'id',
            'name',
            'acronym',
            'billable_minutes',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class ActivityTeamTaskSerializer(RepresentationMixin,
                                 serializers.ModelSerializer):
    """
    serializer for :model:`tasks.TeamTask`
    """

    class Meta:
        model = TeamTask
        fields = (
            'id',
            'plan',
            'team_task_template',
            'status',
        )
        nested_serializers = [
            {
                'field': 'team_task_template',
                'serializer_class': TeamTaskTemplateSerializer,
            },
        ]


class BilledActivitySerializer(RepresentationMixin,
                               serializers.ModelSerializer):
    """
    serializer for :model:`billings.BilledActivity`
    """

    class Meta:
        model = BilledActivity
        fields = (
            'id',
            'plan',
            'activity_type',
            'team_task',
            'members',
            'patient_included',
            'sync_to_ehr',
            'added_by',
            'activity_date',
            'notes',
            'time_spent',
            'readable_time_spent',
            'is_billed',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
        nested_serializers = [
            {
                'field': 'plan',
                'serializer_class': CarePlanSerializer,
            },
            {
                'field': 'members',
                'serializer_class': BasicEmployeeProfileSerializer,
                'many': True,
            },
            {
                'field': 'added_by',
                'serializer_class': BasicEmployeeProfileSerializer
            },
            {
                'field': 'team_task',
                'serializer_class': ActivityTeamTaskSerializer
            },
        ]
