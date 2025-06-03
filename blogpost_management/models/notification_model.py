from django.db import models
from django.contrib.auth import get_user_model

from blogpost_management.models import CommonFields

User = get_user_model()

class Notification(CommonFields):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notification'
        app_label = 'blogpost_management'

