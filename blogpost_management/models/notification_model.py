from django.db import models

from blogpost_management.models import CommonFields
from user_management.models import Users


class Notification(CommonFields):
    recipient = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    event_type = models.CharField(max_length=100,null=True,blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notification'
        app_label = 'blogpost_management'

