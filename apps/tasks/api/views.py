import datetime

import pytz

from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import (
    PatientTaskTemplate,
    PatientTask,
    TeamTaskTemplate,
    TeamTask,
    MedicationTaskTemplate,
    MedicationTask,
    SymptomTaskTemplate,
    SymptomTask,
    SymptomRating,
    AssessmentTaskTemplate,
    AssessmentQuestion,
    AssessmentTask,
    AssessmentResponse,
)
from ..permissions import IsPatientOrEmployeeForTask
from .filters import DurationFilter
from . serializers import (
    PatientTaskTemplateSerializer,
    PatientTaskSerializer,
    PatientTaskTodaySerializer,
    TeamTaskTemplateSerializer,
    TeamTaskSerializer,
    MedicationTaskTemplateSerializer,
    MedicationTaskSerializer,
    MedicationTaskTodaySerializer,
    SymptomTaskTemplateSerializer,
    SymptomTaskSerializer,
    SymptomTaskTodaySerializer,
    SymptomRatingSerializer,
    AssessmentTaskTemplateSerializer,
    AssessmentQuestionSerializer,
    AssessmentTaskSerializer,
    AssessmentTaskTodaySerializer,
    AssessmentResponseSerializer,
)
from care_adopt_backend import utils
from care_adopt_backend.permissions import (
    EmployeeOrReadOnly,
    IsPatientOnly,
)


class PatientTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientTaskTemplate.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get task templates for patients this employee
            # has access to
            return qs.all()
        elif patient_profile is not None:
            patient_plans = patient_profile.care_plans.all()
            plan_templates = patient_plans.values_list("plan_template",
                                                       flat=True)
            return qs.filter(plan_template__id__in=plan_templates)
        else:
            return qs.none()


class PatientTaskViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeForTask,
    )
    queryset = PatientTask.objects.all()
    filter_backends = (DjangoFilterBackend, DurationFilter)
    filterset_fields = (
        'plan__id',
        'patient_task_template__id',
        'plan__patient__id',
        'status',
    )

    def get_queryset(self):
        queryset = super(PatientTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            queryset = queryset.filter(
                plan__care_team_members__employee_profile=user.employee_profile
            )
        elif user.is_patient:
            queryset = queryset.filter(plan__patient=user.patient_profile)

        return queryset


class TeamTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTaskTemplate.objects.all()


class TeamTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTask.objects.all()


class MedicationTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = MedicationTaskTemplate.objects.all()


class MedicationTaskViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsPatientOrEmployeeForTask,
    )
    queryset = MedicationTask.objects.all()

    def get_queryset(self):
        queryset = super(MedicationTaskViewSet, self).get_queryset()
        user = self.request.user

        if user.is_employee:
            queryset = queryset.filter(
                medication_task_template__plan__care_team_members__employee_profile=user.employee_profile
            )
        elif user.is_patient:
            queryset = queryset.filter(medication_task_template__plan__patient=user.patient_profile)

        return queryset


class SymptomTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTaskTemplate.objects.all()


class SymptomTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTask.objects.all()


class SymptomRatingViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomRatingSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomRating.objects.all()


class AssessmentTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentTaskTemplate.objects.all()


class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentQuestionSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentQuestion.objects.all()


class AssessmentTaskViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentTask.objects.all()


class AssessmentResponseViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentResponseSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentResponse.objects.all()


############################
# ----- CUSTOM VIEWS ----- #
############################

class TodaysTasksAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsPatientOnly)

    def get(self, request, format=None):
        tasks = []
        today = timezone.now().date()
        today_min = datetime.datetime.combine(today,
                                              datetime.time.min,
                                              tzinfo=pytz.utc)
        today_max = datetime.datetime.combine(today,
                                              datetime.time.max,
                                              tzinfo=pytz.utc)
        patient_profile = request.user.patient_profile

        patient_tasks = PatientTask.objects.filter(
            plan__patient__id=patient_profile.id,
            due_datetime__range=(today_min, today_max))
        medication_tasks = MedicationTask.objects.filter(
            medication_task_template__plan__patient__id=patient_profile.id,
            due_datetime__range=(today_min, today_max))
        symptom_tasks = SymptomTask.objects.filter(
            plan__patient__id=patient_profile.id,
            due_datetime__range=(today_min, today_max))
        assessment_tasks = AssessmentTask.objects.filter(
            plan__patient__id=patient_profile.id,
            due_datetime__range=(today_min, today_max))

        if patient_tasks.exists():
            serializer = PatientTaskTodaySerializer(
                patient_tasks.all(),
                many=True
            )
            tasks += serializer.data

        if medication_tasks.exists():
            serializer = MedicationTaskTodaySerializer(
                medication_tasks.all(),
                many=True
            )
            tasks += serializer.data

        if symptom_tasks.exists():
            serializer = SymptomTaskTodaySerializer(
                symptom_tasks.all(),
                many=True
            )
            tasks += serializer.data

        if assessment_tasks.exists():
            serializer = AssessmentTaskTodaySerializer(
                assessment_tasks.all(),
                many=True
            )
            tasks += serializer.data

        return Response(data=tasks)
