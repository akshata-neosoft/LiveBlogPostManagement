import uuid
from django.db import models
from blogpost_management.managers.default_manager import DefaultManager
from blogpost_management.models.common_model import CommonFields


class Users(CommonFields):
    """
    This is User models with User Specific Data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email_id = models.EmailField()
    password = models.CharField(max_length=255, null=True, blank=True)
    objects = DefaultManager()


    class Meta:
        db_table = 'users'
        app_label = 'user_management'
