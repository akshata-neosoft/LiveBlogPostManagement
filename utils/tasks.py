from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_follow_notification_task(to_email, post_title):
    send_mail(
        subject="New Post Update",
        message=f"The post '{post_title}' has been updated.",
        from_email="no-reply@example.com",
        recipient_list=[to_email]
    )