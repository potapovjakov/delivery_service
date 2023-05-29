import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_service.settings')

app = Celery('delivery_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every': {
        'task': 'delivery.tasks.update_trucks',
        'schedule': crontab(minute='*/3'),
    },
}
