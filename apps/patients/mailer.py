# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging
import random
import string

from django.apps import apps
from django.conf import settings

from care_adopt_backend.mailer import BaseMailer

logger = logging.getLogger(__name__)


class PatientsMailer(BaseMailer):

    def _generate_verification_code(self, patient):
        code = ''.join(random.choices(
            string.ascii_uppercase + string.digits,
            k=6)
        )

        PatientVerificationCode = apps.get_model(
            'patients',
            'PatientVerificationCode'
        )
        verify = None
        created = False
        while not created:
            verify, created = PatientVerificationCode.objects.get_or_create(
                patient=patient,
                code=code
            )
        return verify

    def send_verification_email(self, patient):
        """
        Sends an email to the patient containing the verification code used
        for creating his/her account.
        """
        verification_code = self._generate_verification_code(patient)
        subject = 'Invitation to CareAdopt'
        context = {
            "patient": patient,
            "verification_code": verification_code,
            "admin_email": settings.DEFAULT_FROM_EMAIL,
        }
        email_template = 'profiles/email/verification_code.html'
        return self.send_mail(
            subject,
            email_template,
            patient.user.email,
            context
        )
