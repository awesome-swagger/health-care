from .mailer import PatientsMailer


def patientprofile_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`patients.PatientProfile`
    """
    if created and instance.is_invited:
        mailer = PatientsMailer()
        mailer.send_verification_email(instance)
    if created and not instance.communication_email:
        instance.communication_email = instance.user.email
        instance.save()
    if instance.is_using_mobile and instance.is_active:
        instance.is_active = False
        instance.save()


def reminder_email_post_save(sender, instance, created, **kwargs):
    if created:
        instance.send_reminder_email()


def emergencycontact_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`patients.EmergencyContact`
    """

    # If instance is primary, mark all other contacts under the same patient
    # as `is_primary=False`
    if instance.is_primary:
        sender.objects.filter(patient=instance.patient).exclude(
            id=instance.id).update(is_primary=False)
