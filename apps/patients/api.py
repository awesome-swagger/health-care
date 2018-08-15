from django.db.models import Q
from rest_framework import serializers, views, viewsets, permissions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.accounts.serializers import SettingsUserForSerializers
from apps.core.models import EmployeeProfile
from apps.patients.models import (
    PatientProfile, PatientDiagnosis, ProblemArea, PatientProcedure,
    PatientMedication, )


class PatientUserInfo(SettingsUserForSerializers, serializers.ModelSerializer):
    class Meta:
        read_only_fields = ('email', 'date_joined', 'last_login', )
        exclude = ('password', 'is_superuser', 'groups', 'user_permissions',
                   'validation_key', 'validated_at', 'reset_key', 'is_developer', )


class PatientSearchUserInfo(SettingsUserForSerializers, serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', )


class PatientSearchSerializer(serializers.ModelSerializer):
    user = PatientSearchUserInfo()

    class Meta:
        model = PatientProfile
        fields = ('id', 'user', )


class PatientProfileSerializer(serializers.ModelSerializer):
    user = PatientUserInfo()

    class Meta:
        model = PatientProfile
        fields = '__all__'


class PatientProfileViewSet(viewsets.ModelViewSet):
    """
    If the requesting user is an employee, this endpoint returns patients that
    belong to the same facilities.

    If the requesting user is a patient, this endpoint only returns their own
    patient profile.
    """
    serializer_class = PatientProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = PatientProfile.objects.all()
        try:
            employee_profile = self.request.user.employee_profile
        except EmployeeProfile.DoesNotExist:
            employee_profile = None
        try:
            patient_profile = self.request.user.patient_profile
        except PatientProfile.DoesNotExist:
            patient_profile = None
        if employee_profile is not None:
            # Filter out users that reqesting user doesn't have access to
            qs = qs.filter(
                Q(facility__id__in=employee_profile.facilities.all()) |
                Q(facility__id__in=employee_profile.facilities_managed.all())
            )
        elif patient_profile is not None:
            # Return only this patient
            qs = qs.filter(user__id=self.request.user.id)
        else:
            qs = qs.none()
        return qs

    @action(methods=['post'], detail=False)
    def search(self, request):
        # TODO: If a user is an organization manager they get all the patients that belong to that organization
        # TODO: If a user is a facility manager they get all the patients that belong to that facility
        # TODO: If a user is not a manager of any organizations/facilities then they can
        # only search for their own patients including the patients they are care managers for
        # or are a member of the care team for.
        # TODO: Need to be able to search by first AND last name (with space)
        search_str = request.data.get('name')
        patients = PatientProfile.objects.filter(
            Q(user__first_name__icontains=search_str) | Q(user__last_name__icontains=search_str))
        serializer = PatientSearchSerializer(patients, many=True)
        return Response(serializer.data)


class PatientDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDiagnosis
        fields = '__all__'


class PatientDiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = PatientDiagnosisSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PatientDiagnosis.objects.all()


class ProblemAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemArea
        fields = '__all__'


class ProblemAreaViewSet(viewsets.ModelViewSet):
    serializer_class = ProblemAreaSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProblemArea.objects.all()


class PatientProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProcedure
        fields = '__all__'


class PatientProcedureViewSet(viewsets.ModelViewSet):
    serializer_class = PatientProcedureSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PatientProcedure.objects.all()


class PatientMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedication
        fields = '__all__'


class PatientMedicationViewSet(viewsets.ModelViewSet):
    serializer_class = PatientMedicationSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PatientMedication.objects.all()
