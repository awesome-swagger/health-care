import datetime
import os
import uuid
import hashlib
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.urls import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def get_placeholder_url(request=None) -> str:
    """
    Return a URL for the placeholder profile image, typically used when
    no custom image exists for a user.

    If a request object is provided, it will be used to construct an
    absolute URL; if no request passed, an absolute URL is constructed
    via settings.SITE_DOMAIN and settings.SITE_SCHEMA if possible.
    If all else fails, then a relative URL is returned.
    """
    url = '{}accounts/images/placeholder_profile.png'.format(settings.STATIC_URL)
    if request:
        return '{}://{}{}'.format(request.scheme, request.get_host(), url)
    elif getattr(settings, 'SITE_DOMAIN', None):
        return '{schema}://{domain}{path}'.format(
            schema=getattr(settings, 'SITE_SCHEMA', 'http'),
            domain=settings.SITE_DOMAIN,
            path=url,
        )
    return url


def get_gravatar_url(email, size=80, secure=True, default='mm'):
    if secure:
        url_base = 'https://secure.gravatar.com/'
    else:
        url_base = 'http://www.gravatar.com/'
    email_hash = hashlib.md5(email.encode('utf-8').strip().lower()).hexdigest()
    qs = urlencode({
        's': str(size),
        'd': default,
        'r': 'pg',
    })
    url = '{}avatar/{}.jpg?{}'.format(url_base, email_hash, qs)
    return url


def has_gravatar(email):
    url = get_gravatar_url(email, default='404')
    try:
        request = Request(url)
        request.get_method = lambda: 'HEAD'
        return 200 == urlopen(request).code
    except (HTTPError, URLError):
        return False


def user_image_upload_to(user, filename):
    """Upload images to a sensible location."""
    ext = os.path.splitext(filename)[-1]
    if filename == 'blob':
        ext = '.png'
    return 'users/{}/profile{}'.format(
        user.email, ext
    )


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password=None, is_superuser=False, **kwargs):
        user = self.model(email=email, is_superuser=is_superuser, **kwargs)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        return self._create_user(email, password, is_superuser=False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, is_superuser=True, **kwargs)


class EmailUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        ('f', 'Female'),
        ('m', 'Male'),
    ]

    # Use a UUID for a primary key
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User information
    email = models.EmailField(_('email address'), unique=True, blank=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    image = models.ImageField(
        upload_to=user_image_upload_to, blank=True, null=True)
    preferred_name = models.CharField(max_length=30, blank=True)
    gender = models.CharField(
        null=True, blank=True, max_length=1, choices=GENDER_CHOICES,
        default=None)
    birthdate = models.DateField(
        null=True, blank=True, verbose_name='Birth date')
    phone = models.CharField(
        max_length=16, blank=True, verbose_name='Phone number')

    # Account Validation
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    validated_at = models.DateTimeField(null=True, blank=True)
    validation_key = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    reset_key = models.UUIDField(default=None, null=True, blank=True)

    # Permissions
    is_developer = models.BooleanField(
        default=False, verbose_name='Developer',
        help_text='User can see developer settings on the frontend clients.')

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    objects = EmailUserManager()

    # Core Django Functionality
    def get_full_name(self):
        """Returns first_name plus last_name, with a space in between."""
        full_name = '{} {}'.format(self.first_name, self.last_name).strip()
        return full_name or self.email

    def get_short_name(self):
        """Returns the short name for the User."""
        return self.first_name or self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_staff(self):
        return self.is_superuser

    # Some nice conveniences
    @property
    def age(self) -> int:
        """
        Returns the person's age in years, or zero if there is no
        birthdate.
        """
        if not self.birthdate:
            return 0
        # TODO: make this calculation better
        # noinspection PyTypeChecker
        return (datetime.date.today() - self.birthdate).days // 365

    def _send_html_mail(self, subject, template_html, template_text, **context):
        """
        Renders templates to context, and uses EmailMultiAlternatives to
        send email.
        """
        if not template_html:
            raise ValueError('No HTML template provided for email.')
        if not template_text:
            raise ValueError('No text template provided for email.')
        default_context = {
            "settings": settings,
            "user": self
        }
        default_context.update(context)
        from_email = settings.DEFAULT_FROM_EMAIL
        body_text = render_to_string(template_text, default_context)
        body_html = render_to_string(template_html, default_context)

        msg = EmailMultiAlternatives(
            subject=subject, body=body_text,
            from_email=from_email, to=[self.email])
        msg.attach_alternative(body_html, 'text/html')
        msg.send()

    # Get the profile pic
    def get_image_url(self, request=None) -> str:
        """
        Get the profile image url for this user if it exists.
        If not, return either their gravatar url or the placeholder image url.
        """
        if not self.image:
            if has_gravatar(self.email):
                return get_gravatar_url(self.email, size=256)
            return get_placeholder_url(request=request)
        else:
            url = self.image.url
        if request:
            return '{}://{}{}'.format(request.scheme, request.get_host(), url)
        return url

    def image_tag(self) -> str:
        """Returns html tag with user image. Used on admin page"""
        return '<img src="{}"  height="20"/>'.format(self.get_image_url())
    image_tag.short_description = 'Thumbnail'
    image_tag.allow_tags = True

    # Set the user as active
    def validate(self) -> None:
        """
        Marks a user as validated and sends a confirmation email, clearing the
        validation_key so the validation link only works once.
        """
        self.validation_key = None
        self.validated_at = timezone.now()
        self.save()
        self._send_html_mail(
            'Your account has been validated',
            'email/user_validated.html',
            'email/user_validated.txt')

    def send_validation_email(self):
        """
        Send email with a unique link using validation_key to validate account.
        """
        self.validation_key = uuid.uuid4()
        self.save()
        self._send_html_mail(
            'Please validate your email address',
            'email/user_validation.html',
            'email/user_validation.txt',
            url=settings.SITE_DOMAIN + reverse(
                'user-validation',
                kwargs={"validation_key": self.validation_key})
        )

    def send_reset_password_email(self, request):
        """
        Send email with unique link to reset password. Create a new
        validation_key, which will be cleared once password is reset.
        """
        self.reset_key = uuid.uuid4()
        self.save()
        self._send_html_mail(
            'Password Reset Request',
            'email/user_reset_password.html',
            'email/user_reset_password.txt',
            url=settings.SITE_DOMAIN + reverse(
                'reset-request',
                kwargs={"reset_key": self.reset_key})
        )

    def send_reset_password_success_email(self):
        """
        Send email notifying users that their password was successfully reset.
        Validation key is cleared so the reset password link only works once.
        """
        self.reset_key = None
        self.save()
        self._send_html_mail(
            'Password successfully changed',
            'email/user_reset_password_success.html',
            'email/user_reset_password_success.txt')


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def validate_new_user(sender, instance, created, **kwargs):
    """Send a validation email when a new user is created."""
    if created and not instance.validated_at:
        instance.send_validation_email()
