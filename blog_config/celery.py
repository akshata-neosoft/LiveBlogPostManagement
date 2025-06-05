# project_root/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_config.settings')

app = Celery('blog_config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
