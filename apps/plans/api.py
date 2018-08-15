from rest_framework import serializers, viewsets, permissions, mixins
from apps.plans.models import (
    CarePlanTemplate, CarePlanInstance, PlanConsent, Goal, TeamTask, PatientTask,
    MessageStream, StreamMessage, )


class CarePlanTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlanTemplate
        fields = '__all__'


class CarePlanTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = CarePlanTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = CarePlanTemplate.objects.all()


class CarePlanInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarePlanInstance
        fields = '__all__'


class CarePlanInstanceViewSet(viewsets.ModelViewSet):
    serializer_class = CarePlanInstanceSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = CarePlanInstance.objects.all()


class PlanConsentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlanConsent
        fields = '__all__'


class PlanConsentViewSet(viewsets.ModelViewSet):
    serializer_class = PlanConsentSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PlanConsent.objects.all()


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
