from rest_framework import serializers, viewsets, permissions, mixins
from apps.plans.models import (
    CarePlanTemplate, CarePlanInstance, PlanConsent, Goal, TeamTask, PatientTask,
    MessageStream, StreamMessage, )
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
    permission_classes = (permissions.IsAuthenticated, )

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
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = PlanConsent.objects.all()
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)
        if employee_profile is not None:
            return qs.all()
        if patient_profile is not None:
            return qs.filter(plan_instance__in=patient_profile.care_plans.all())
        return PlanConsent.objects.none()


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = '__all__'


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Goal.objects.all()


class TeamTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTask
        fields = '__all__'


class TeamTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = TeamTask.objects.all()


class PatientTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientTask
        fields = '__all__'


class PatientTaskViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PatientTask.objects.all()


class MessageStreamSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageStream
        fields = '__all__'


class MessageStreamViewSet(viewsets.ModelViewSet):
    serializer_class = MessageStreamSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = MessageStream.objects.all()


class StreamMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = StreamMessage
        fields = '__all__'


class StreamMessageViewSet(viewsets.ModelViewSet):
    serializer_class = StreamMessageSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = StreamMessage.objects.all()
