import uuid
from django.db import models


class CreatedModifiedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class AddressMixin(models.Model):
    addr_street = models.CharField(max_length=255, null=True, blank=True)
    addr_suite = models.CharField(max_length=35, null=True, blank=True)
    addr_city = models.CharField(max_length=255, null=True, blank=True)
    addr_state = models.CharField(max_length=255, null=True, blank=True)
    addr_zip = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        abstract = True
