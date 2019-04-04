from django.utils import timezone


class DestroyTemplateMixin(object):
    """
    Custom delete behavior for Task Template models.
    This mixin will do the following:

        - remove all task after the current date
        - mark the template as inactive (`is_active=False`)
    """

    def perform_destroy(self, instance):
        now = timezone.now()

        task_model = getattr(instance, self.task_field, None)

        if task_model:
            task_model.filter(due_datetime__gte=now).delete()

        instance.is_active = False
        instance.save(update_fields=['is_active'])
