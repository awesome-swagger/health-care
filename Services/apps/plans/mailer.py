# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.conf import settings

from care_adopt_backend.mailer import BaseMailer

logger = logging.getLogger(__name__)


class PlansMailer(BaseMailer):

    def notify_old_billing_practitioner(self, plan, old_practitioner):
        """
        Sends an email to the old billing practitioner informing him/her
        that he/she has been changed.
        """
        subject = 'Notification from CareAdopt'
        context = {
            "plan": plan,
            "subject": subject,
            "admin_email": settings.DEFAULT_FROM_EMAIL,
        }
        email_template = 'core/employeeprofile/email/billing_practitioner.html'
        return BaseMailer().send_mail(
            subject,
            email_template,
            old_practitioner.user.email,
            context
        )
