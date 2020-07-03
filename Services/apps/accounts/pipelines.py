from django.utils import timezone


def validate(strategy, user, response, details, is_new=False, *args, **kwargs):
    if not user.validated_at:
        user.validated_at = timezone.now()
        user.save()
