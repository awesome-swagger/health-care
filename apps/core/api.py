from django.db.models import Q
from rest_framework import serializers, viewsets, permissions, mixins
from apps.core.models import (
    Organization, Facility, ProviderProfile, ProviderTitle, ProviderRole,
    ProviderSpecialty, Diagnosis)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        qs = Organization.objects.none()
        provider_profile = self.request.user.provider_profile
        if provider_profile is not None:
            qs = Organization.objects.filter(
                Q(id__in=provider_profile.organizations.all()) |
                Q(id__in=provider_profile.organizations_managed.all())
            )
            return qs
        patient_profile = self.request.user.patient_profile
        if patient_profile is not None:
            qs = Organization.objects.filter(
                id=patient_profile.facility.organization.id)
        return qs


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = '__all__'


class FacilityViewSet(viewsets.ModelViewSet):
    serializer_class = FacilitySerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Facility.objects.all()


class ProviderProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderProfile
        fields = '__all__'


class ProviderProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProviderProfile.objects.all()


class ProviderTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderTitle
        fields = '__all__'


class ProviderTitleViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderTitleSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProviderTitle.objects.all()


class ProviderRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderRole
        fields = '__all__'


class ProviderRoleViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderRoleSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProviderRole.objects.all()


class ProviderSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderSpecialty
        fields = '__all__'


class ProviderSpecialtyViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSpecialtySerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = ProviderSpecialty.objects.all()


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = '__all__'


class DiagnosisViewSet(viewsets.ModelViewSet):
    serializer_class = DiagnosisSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Diagnosis.objects.all()
