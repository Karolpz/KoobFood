from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'koobfood.settings')

app = Celery('koobfood')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
