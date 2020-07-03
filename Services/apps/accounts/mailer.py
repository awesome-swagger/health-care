# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_auth.models import TokenModel

from care_adopt_backend.mailer import BaseMailer

logger = logging.getLogger(__name__)


class UserMailer(BaseMailer):

    def _generate_uidb64_token(self, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token, _ = TokenModel.objects.get_or_create(user=user)
        return (uidb64, token.key)

    def send_change_email_verification(self, user):
        """
        Sends email to user when invoking the change email form.
        """
        uidb64, token = self._generate_uidb64_token(user)
        subject = 'CareAdopt - Change Email'

        context = {
            "user": user,
            "uidb64": uidb64,
            "token": token,
            "current_site": "http://localhost:8000",  # change this later
        }
        email_template = 'accounts/emailuser/email/change_email.html'
        return self.send_mail(
            subject,
            email_template,
            user.email,
            context
        )
