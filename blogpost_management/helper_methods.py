import json

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
from django.dispatch import receiver

from user_management.models import Users
from .models import Comment
from .models.notification_model import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.core.mail import send_mail
from utils.tasks import send_follow_notification_task



def notify_user(user, message, event_type="info", related_object=None):
    recipent_obj= Users.objects.filter(id=str(user.id)).exclude(status=2).first()
    Notification.objects.create(
        recipient=recipent_obj,
        message=message,
        event_type=event_type
    )

def notify_ws_clients(event_type, blog_data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'live_blogs',
        {
            'type': 'blog_post_event',
            'data': {
                'event': event_type,
                'post': json.loads(json.dumps(blog_data, cls=DjangoJSONEncoder))
            }
        }
    )




@receiver(post_save, sender=Comment)
def notify_user_on_comment(sender, instance, created, **kwargs):
    if created:
        notify_user(instance.blog_post.author, f"Your post '{instance.blog_post.title}' received a new comment.")




def send_follow_notification(to_user, post):
    send_follow_notification_task.delay(to_user.email_id, post.title)
    send_mail(
        subject="New Post Update",
        message=f"The post '{post.title}' has been updated.",
        from_email="no-reply@example.com",
        recipient_list=[to_user.email_id]
    )