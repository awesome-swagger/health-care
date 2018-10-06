from django.utils.translation import ugettext_lazy as _

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


class InfoMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoMessage
        fields = (
            'id',
            'queue',
            'text',
        )
        read_only_fields = (
            'id',
        )


class InfoMessageQueueSerializer(serializers.ModelSerializer):

    messages = InfoMessageSerializer(many=True, read_only=True)

    class Meta:
        model = InfoMessageQueue
        fields = (
            'id',
            'plan_template',
            'name',
            'type',
            'messages',
            'created',
            'modified'
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


class SimplifiedGoalProgressSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalProgress`. This will be primarily
    used as an inline in GoalSerializer.
    """
    goal_name = serializers.SerializerMethodField()

    class Meta:
        model = GoalProgress
        fields = (
            'id',
            'goal_name',
            'rating',
            'created',
        )
        read_only_fields = (
            'id',
            'goal_name',
            'rating',
            'created',
        )

    def get_goal_name(self, obj):
        return obj.goal.goal_template.name


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

    def validate(self, data):
        goal = data['goal'] if 'goal' in data else self.instance.goal
        user = data['user'] if 'user' in data else self.instance.user

        if user.is_superuser:
            return data
        elif user.is_employee:
            profiles = goal.plan.care_team_members.values_list(
                'employee_profile', flat=True).distinct()
            if user.employee_profile.id not in profiles:
                err = _(
                    "The user is not a care team member of the goal provided."
                )
                raise serializers.ValidationError(err)
            return data
        elif user.is_patient:
            patient = user.patient_profile
            if goal.plan.patient != patient:
                err = _("The user is not the owner of the goal's plan.")
                raise serializers.ValidationError(err)
            return data


class SimplifiedGoalCommentSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.GoalComment`. This will be primarily
    used as an inline in GoalSerializer.
    """

    class Meta:
        model = GoalComment
        fields = (
            'id',
            'user',
            'content',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'user',
            'content',
            'created',
            'modified',
        )


class GoalSerializer(serializers.ModelSerializer):
    """
    serializer for :model:`plans.Goal`
    """
    latest_progress = SimplifiedGoalProgressSerializer(read_only=True)
    comments = SimplifiedGoalCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Goal
        fields = (
            'id',
            'plan',
            'goal_template',
            'latest_progress',
            'comments',
            'start_on_datetime',
            'created',
            'modified',
        )
        read_only_fields = (
            'id',
            'created',
            'modified',
        )


class CarePlanGoalSerializer(serializers.ModelSerializer):
    """
    serializer to be used by :model:`plans.CarePlan` with
    corresponding related goal objects.
    """
    goals = SimplifiedGoalProgressSerializer(many=True)
    plan_template = CarePlanTemplateSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'plan_template',
            'goals',
        )
