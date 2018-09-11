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
    PatientTaskInstance,
    TeamTaskTemplate,
    TeamTaskInstance,
    MedicationTaskTemplate,
    MedicationTaskInstance,
    SymptomTaskTemplate,
    SymptomTaskInstance,
    SymptomRating,
    AssessmentTaskTemplate,
    AssessmentQuestion,
    AssessmentTaskInstance,
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


class TeamTaskInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamTaskInstance
        fields = '__all__'


class TeamTaskInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = TeamTaskInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = TeamTaskInstance.objects.all()


class MedicationTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationTaskTemplate
        fields = '__all__'


class MedicationTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = MedicationTaskTemplate.objects.all()


class MedicationTaskInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = MedicationTaskInstance
        fields = '__all__'


class MedicationTaskInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = MedicationTaskInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = MedicationTaskInstance.objects.all()


class SymptomTaskTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTaskTemplate
        fields = '__all__'


class SymptomTaskTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTaskTemplate.objects.all()


class SymptomTaskInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = SymptomTaskInstance
        fields = '__all__'


class SymptomTaskInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = SymptomTaskInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = SymptomTaskInstance.objects.all()


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


class AssessmentTaskInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssessmentTaskInstance
        fields = '__all__'


class AssessmentTaskInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentTaskInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, EmployeeOrReadOnly, )
    queryset = AssessmentTaskInstance.objects.all()


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
