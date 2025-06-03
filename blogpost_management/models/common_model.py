from django.db import models
from .domain_model import Status
from ..managers.default_manager import DefaultManager


class CommonFields(models.Model):
    # Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True)
    created_at_epoch = models.IntegerField(null=True)
    created_by = models.CharField(max_length=255, null=True, blank=True)
    updated_by = models.CharField(max_length=255, null=True, blank=True)
    deleted_by = models.CharField(max_length=255, null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True,
                               blank=True)

    # Managers
    objects = DefaultManager()

    # Meta
    class Meta:
        abstract = True
