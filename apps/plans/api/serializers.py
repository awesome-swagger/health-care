from rest_framework import serializers

from ..models import (
    CarePlanTemplate,
    CarePlan,
    PlanConsent,
    GoalTemplate,
    Goal,
    GoalProgress,
    GoalComment,
    InfoMessageQueue,
    InfoMessage,
    CareTeamMember,
)
from apps.core.api.serializers import (
    ProviderRoleSerializer,
    EmployeeProfileSerializer,
)


class CarePlanTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlanTemplate
        fields = '__all__'


class CarePlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlan
        fields = '__all__'


class PlanConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanConsent
        fields = '__all__'


class CareTeamMemberSerializer(serializers.ModelSerializer):
    employee_profile = EmployeeProfileSerializer(many=False)
    role = ProviderRoleSerializer(many=False)
    plan = CarePlanSerializer(many=False)

    class Meta:
        model = CareTeamMember
        fields = '__all__'


class GoalTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalTemplate
        fields = '__all__'


class InfoMessageQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoMessageQueue
        fields = '__all__'


class InfoMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoMessage
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.Goal`
    """

    class Meta:
        model = Goal
        fields = (
            'id',
            'plan',
            'goal_template',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class GoalProgressSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalProgress`
    """

    class Meta:
        model = GoalProgress
        fields = (
            'id',
            'goal',
            'rating',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class GoalCommentSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalComment`
    """

    class Meta:
        model = GoalComment
        fields = (
            'id',
            'goal',
            'user',
            'content',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )
