import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


class BaseMailer(object):
    """
    base class for sending emails

    """
    def __init__(self, request=None):
        self.request = request

    def send_mail(self, subject, template_name, email, context):
        try:
            msg = self.render_mail(subject, template_name, email, context)
            msg.send()
            return True
        except Exception as ex:
            logger.error(ex)
            return False

    def render_mail(self, subject, template_name, email, context):
        from_email = settings.DEFAULT_FROM_EMAIL
        body = render_to_string(template_name, context).strip()
        msg = EmailMessage(
            subject,
            body,
            from_email,
            [email]
        )
        msg.content_subtype = 'html'  # Main content is now text/html
        return msg
