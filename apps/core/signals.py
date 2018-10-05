def invited_email_template_post_save(sender, instance, created, **kwargs):
    if created:
        sender.objects.exclude(id=instance.id).update(is_default=False)
