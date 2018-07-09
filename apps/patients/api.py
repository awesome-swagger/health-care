from django.db.models import Q
from rest_framework import serializers, viewsets, permissions, mixins
from apps.core.models import ProviderProfile
from apps.patients.models import (
    PatientProfile, PatientDiagnosis, ProblemArea, PatientProcedure, )


class PatientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfile
        fields = '__all__'


class PatientProfileViewSet(viewsets.ModelViewSet):
    serializer_class = PatientProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = PatientProfile.objects.all()
        try:
            provider_profile = self.request.user.provider_profile
        except ProviderProfile.DoesNotExist:
            provider_profile = None
        try:
            patient_profile = self.request.user.patient_profile
        except PatientProfile.DoesNotExist:
            patient_profile = None
        if provider_profile is not None:
            # Filter out users that this provider is not apart of
            qs = qs.filter(
                Q(facility__id__in=provider_profile.facilities.all()) |
                Q(facility__id__in=provider_profile.facilities_managed.all())
            )
        elif patient_profile is not None:
            # Return only this patient
            qs = qs.filter(user__id=self.request.user.id)
        else:
            qs = qs.none()
        return qs


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
