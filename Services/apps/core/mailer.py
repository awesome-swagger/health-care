# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.conf import settings

from care_adopt_backend.mailer import BaseMailer

logger = logging.getLogger(__name__)


class EmployeeMailer(BaseMailer):

    def send_invitation(self, employee, pre_content=''):
        """
        Sends an email invitation to the employee
        """
        facility = employee.facilities.first()
        organization = employee.organizations.first()
        employer = f'{facility.name} ({organization.name})' \
            if facility else organization.name
        subject = f'Invitation from {employer}'
        context = {
            "subject": subject,
            "employee": employee,
            "pre_content": pre_content,
            "admin_email": settings.DEFAULT_FROM_EMAIL,
        }
        email_template = 'core/employeeprofile/email/send_invitation.html'
        return self.send_mail(
            subject,
            email_template,
            employee.user.email,
            context
        )
