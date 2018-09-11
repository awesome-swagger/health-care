from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from care_adopt_backend.permissions import EmployeeOrReadOnly
from apps.core.models import (ProviderRole, )
from apps.core.api import (ProviderRoleSerializer, EmployeeProfileSerializer, )
from apps.plans.models import (
    CarePlanTemplate, CarePlanInstance, PlanConsent, GoalTemplate, InfoMessageQueue,
    InfoMessage, CareTeamMember, )
from care_adopt_backend import utils


class CarePlanTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlanTemplate
        fields = '__all__'


class CarePlanTemplateViewSet(viewsets.ModelViewSet):
    """
    Permissions
    ========
    Employees get all templates, patients only get templates for which they have an
    existing plan instance for.

    Employees are able to create and update templates.  They are read-only for patients.
    """
    serializer_class = CarePlanTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )

    def get_queryset(self):
        qs = CarePlanTemplate.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            return qs.all()
        if patient_profile is not None:
            template_ids = patient_profile.care_plans.all().values_list(
                'plan_template', flat=True)
            return qs.filter(
                id__in=template_ids)
        return CarePlanTemplate.objects.none()


class CarePlanInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlanInstance
        fields = '__all__'


class CarePlanInstanceViewSet(viewsets.ModelViewSet):
    """
    Permissions
    ========
    Employees get all care plans, patients only get the ones they're assigned to.
    """
    serializer_class = CarePlanInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = CarePlanInstance.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            return qs.all()
        if patient_profile is not None:
            return patient_profile.care_plans.all()
        return CarePlanInstance.objects.none()

    @action(methods=['get'], detail=True)
    def care_team_members(self, request, pk=None):
        plan = CarePlanInstance.objects.get(id=pk)
        care_team_members = plan.care_team_members
        serializer = CareTeamMemberSerializer(care_team_members, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def available_roles(self, request, pk=None):
        plan = CarePlanInstance.objects.get(id=pk)
        template = plan.plan_template
        care_team_members = plan.care_team_members
        all_roles = list(template.team_tasks.filter(
            role__isnull=False).values_list('role', flat=True).distinct())
        assigned_roles = list(care_team_members.filter(
                role__isnull=False).values_list('role', flat=True).distinct())
        available_roles = ProviderRole.objects.filter(
            id__in=list(set(all_roles) - set(assigned_roles)))
        serializer = ProviderRoleSerializer(available_roles, many=True)
        return Response(serializer.data)


class PlanConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanConsent
        fields = '__all__'


class PlanConsentViewSet(viewsets.ModelViewSet):
    """
    Permissions
    ========
    Employees get all consent forms, patients only get their own.
    """
    serializer_class = PlanConsentSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )

    def get_queryset(self):
        qs = PlanConsent.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            return qs.all()
        if patient_profile is not None:
            return qs.filter(plan_instance__in=patient_profile.care_plans.all())
        return PlanConsent.objects.none()


class CareTeamMemberSerializer(serializers.ModelSerializer):
    employee_profile = EmployeeProfileSerializer(many=False)
    role = ProviderRoleSerializer(many=False)
    plan_instance = CarePlanInstanceSerializer(many=False)

    class Meta:
        model = CareTeamMember
        fields = '__all__'


class CareTeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = CareTeamMemberSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )

    def get_queryset(self):
        qs = CareTeamMember.objects.all()

        plan_instance = self.request.query_params.get('plan')
        if plan_instance:
            qs = qs.filter(plan_instance=plan_instance)
        employee_param = self.request.query_params.get('employee')
        if employee_param:
            qs = qs.filter(employee_profile=employee_param)

        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            qs = qs.all()
        elif patient_profile is not None:
            qs = qs.filter(
                plan_instance__patient=patient_profile)
        else:
            return qs.none()
        return qs


class GoalTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoalTemplate
        fields = '__all__'


class GoalTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = GoalTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = GoalTemplate.objects.all()


class InfoMessageQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoMessageQueue
        fields = '__all__'


class InfoMessageQueueViewSet(viewsets.ModelViewSet):
    serializer_class = InfoMessageQueueSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = InfoMessageQueue.objects.all()


class InfoMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = InfoMessage
        fields = '__all__'


class InfoMessageViewSet(viewsets.ModelViewSet):
    serializer_class = InfoMessageSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = InfoMessage.objects.all()
