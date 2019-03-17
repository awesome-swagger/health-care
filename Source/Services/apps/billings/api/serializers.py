from rest_framework import serializers

from ..models import BilledActivity, BillingType
from apps.core.api.mixins import RepresentationMixin
from apps.core.api.serializers import BasicEmployeeProfileSerializer
from apps.plans.api.serializers import CarePlanSerializer
from apps.tasks.models import TeamTaskTemplate


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


class ActivityTeamTaskTemplateSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`tasks.TeamTaskTemplate`
    """

    class Meta:
        model = TeamTaskTemplate
        fields = (
            'id',
            'plan_template',
            'name',
            'is_manager_task',
            'category',
            'role',
            'start_on_day',
            'frequency',
            'repeat_amount',
            'appear_time',
            'due_time',
        )


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
            'team_task_template',
            'members',
            'patient_included',
            'sync_to_ehr',
            'added_by',
            'activity_datetime',
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
                'field': 'team_task_template',
                'serializer_class': ActivityTeamTaskTemplateSerializer
            },
        ]
