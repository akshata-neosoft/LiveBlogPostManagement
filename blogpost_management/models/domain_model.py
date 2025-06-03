from django.db import models

from ..managers.domain_manager import DomainManager


class DomainTable(models.Model):
    # Fields
    id = models.IntegerField(primary_key=True, editable=False)
    value = models.CharField(max_length=255, unique=True, null=True)
    description = models.CharField(max_length=255, null=True)

    # Managers
    objects = DomainManager()

    # Meta
    class Meta:
        abstract = True

    # Functions
    def __str__(self):
        return self.value

    @classmethod
    def default(cls):
        return cls.objects.get(pk=0)


class Status(DomainTable):
    # Meta
    class Meta:
        db_table = 'status'
        app_label = 'blogpost_management'

    # Methods
    @classmethod
    def deleted(cls):
        return cls.objects.get(pk=2)

    @classmethod
    def non_deleted(cls):
        return cls.objects.exclude(pk=2)
