import datetime
from rest_framework import serializers, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from care_adopt_backend.permissions import EmployeeOrReadOnly
from apps.core.models import (ProviderRole, )
from apps.core.api import (ProviderRoleSerializer, EmployeeProfileSerializer, )
from apps.tasks.models import (
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


class PatientTaskSerializer(serializers.ModelSerializer):
    patient_task_template = PatientTaskTemplateSerializer(many=False)

    class Meta:
        model = PatientTask
        fields = '__all__'


class PatientTaskViewSet(viewsets.ModelViewSet):
    serializer_class = PatientTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = PatientTask.objects.all()

    def get_queryset(self):
        qs = self.queryset
        employee_profile = utils.employee_profile_or_none(self.request.user)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if employee_profile is not None:
            # TODO: Only get tasks for patients this employee has access to
            return qs.all()
        elif patient_profile is not None:
            return qs.filter(plan__patient__id=patient_profile.id)
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


class TeamTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTask
        fields = '__all__'


class TeamTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTask.objects.all()


class MedicationTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationTaskTemplate
        fields = '__all__'


class MedicationTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = MedicationTaskTemplate.objects.all()


class MedicationTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationTask
        fields = '__all__'


class MedicationTaskViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = MedicationTask.objects.all()


class SymptomTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTaskTemplate
        fields = '__all__'


class SymptomTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTaskTemplate.objects.all()


class SymptomTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTask
        fields = '__all__'


class SymptomTaskViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTask.objects.all()


class SymptomRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomRating
        fields = '__all__'


class SymptomRatingViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomRatingSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomRating.objects.all()


class AssessmentTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentTaskTemplate
        fields = '__all__'


class AssessmentTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentTaskTemplate.objects.all()


class AssessmentQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentQuestion
        fields = '__all__'


class AssessmentQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentQuestionSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentQuestion.objects.all()


class AssessmentTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentTask
        fields = '__all__'


class AssessmentTaskViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentTask.objects.all()


class AssessmentResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentResponse
        fields = '__all__'


class AssessmentResponseViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentResponseSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentResponse.objects.all()


class TodaysTasksAPIView(APIView):

    def get(self, request, format=None):
        tasks = []
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        patient_profile = utils.patient_profile_or_none(self.request.user)

        if patient_profile is not None:
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
            for task in patient_tasks.all():
                tasks.append({
                    'id': task.id,
                    'type': 'patient_task',
                    'name': task.patient_task_template.name,
                    'appear_datetime': task.appear_datetime,
                    'due_datetime': task.due_datetime,
                })
            for task in medication_tasks.all():
                name = '{}, {}mg'.format(
                    task.medication_task_template.patient_medication.medication.name,
                    task.medication_task_template.patient_medication.dose_mg,
                )
                tasks.append({
                    'id': task.id,
                    'type': 'medication_task',
                    'name': name,
                    'appear_datetime': task.appear_datetime,
                    'due_datetime': task.due_datetime,
                })
            for task in symptom_tasks.all():
                tasks.append({
                    'id': task.id,
                    'type': 'symptom_task',
                    'name': 'Symptoms Report',
                    'appear_datetime': task.appear_datetime,
                    'due_datetime': task.due_datetime,
                })
            for task in assessment_tasks.all():
                tasks.append({
                    'id': task.id,
                    'type': 'assessment_task',
                    'name': task.assessment_task_template.name,
                    'appear_datetime': task.appear_datetime,
                    'due_datetime': task.due_datetime,
                })
            return Response(tasks)
