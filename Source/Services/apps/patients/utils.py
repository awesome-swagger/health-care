from apps.plans.models import (
    CarePlan,
)
from apps.plans.api.serializers import (
    CarePlanSerializer,
)

def get_all_plans_for_patient(patient):
    """

    """
    plans = []
    patient_plans = CarePlan.objects.all()

    if patient_plans.exists():
        serializer = CarePlanSerializer(
            patient_plans.all(),
            many=True
        )
        plans += serializer.data

    return plans
