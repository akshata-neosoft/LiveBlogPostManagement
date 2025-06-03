import time
from django.db import models
from ..models.domain_model import Status


class DefaultManager(models.Manager):
    def create_with_defaults(self, *args, **kwargs):
        """Adding created_at_epoc for sorting"""
        kwargs['created_at_epoch'] = int(time.time())
        return self.create(status=Status.default(), *args, **kwargs)

    def get_api_queryset(self):
        return self.exclude(status=2)

    def get_or_create_with_defaults(self, *args, **kwargs):
        """Adding created_at_epoch for sorting"""

        kwargs['defaults'] = kwargs.get('defaults', {})
        kwargs['defaults']['created_at_epoch'] = int(time.time())
        kwargs['defaults']['status'] = kwargs['defaults'].get('status', Status.default())
        return super().get_or_create(*args, **kwargs)

