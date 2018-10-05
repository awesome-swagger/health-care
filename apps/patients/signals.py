def reminder_email_post_save(sender, instance, created, **kwargs):
    if created:
        instance.send_reminder_email()