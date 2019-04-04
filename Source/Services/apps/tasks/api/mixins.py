from django.utils import timezone


class DestroyTemplateMixin(object):

    def perform_destroy(self, instance):
        now = timezone.now()

        task_model = getattr(instance, self.task_field, None)

        if task_model:
            task_model.filter(due_datetime__gte=now).delete()

        instance.is_active = False
        instance.save(update_fields=['is_active'])
