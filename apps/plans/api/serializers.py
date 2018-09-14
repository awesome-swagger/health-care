from rest_framework import serializers

from ..models import (
    CarePlanTemplate,
    CarePlan,
    PlanConsent,
    GoalTemplate,
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
