import datetime
from rest_framework import serializers, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from care_adopt_backend.permissions import EmployeeOrReadOnly
from apps.core.models import (ProviderRole, )
from apps.core.api import (ProviderRoleSerializer, EmployeeProfileSerializer, )
from apps.tasks.models import (
    PatientTaskTemplate, PatientTaskInstance, TeamTaskTemplate, )
from care_adopt_backend import utils


class PatientTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientTaskTemplate
        fields = '__all__'


class PatientTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientTaskTemplate.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get task templates for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            patient_plans = patient_profile.care_plans.all()
            plan_templates = patient_plans.values_list("plan_template", flat=True)
            return qs.filter(plan_template__id__in=plan_templates)
        else:
            return qs.none()


class PatientTaskInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientTaskInstance
        fields = '__all__'


class PatientTaskInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientTaskInstance.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get tasks for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            return qs.filter(plan_instance__patient__id=patient_profile.id)
        else:
            return qs.none()


class TeamTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTaskTemplate
        fields = '__all__'


class TeamTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTaskTemplate.objects.all()


class TodaysTasksAPIView(APIView):

    def get(self, request, format=None):
        tasks = []
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if patient_profile is not None:
            patient_tasks = PatientTaskInstance.objects.filter(
                plan_instance__patient__id=patient_profile.id,
                due_datetime__range=(today_min, today_max))
            medication_tasks = MedicationTaskInstance.objects.filter()
            for task in patient_tasks.all():
                tasks.append({
                    'id': task.id,
                    'type': 'patient_task',
                    'name': task.patient_task_template.name,
                    'appear_datetime': task.appear_datetime,
                    'due_datetime': task.due_datetime,
                })
            return Response(tasks)
