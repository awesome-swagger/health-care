from .mailer import PatientsMailer


def patientprofile_post_save(sender, instance, created, **kwargs):
    """
    Function to be used as signal (post_save) when saving
    :model:`patients.PatientProfile`
    """
    if created and instance.is_invited:
        mailer = PatientsMailer()
        mailer.send_verification_email(instance)


def reminder_email_post_save(sender, instance, created, **kwargs):
    if created:
        instance.send_reminder_email()
