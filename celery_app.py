import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delivery_service.settings')

app = Celery('delivery_service')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def update_trucks():
    from delivery.services import auto_update_tracks_location

    auto_update_tracks_location()


app.conf.beat_schedule = {
    'every': {
        'task': 'celery_app.update_trucks',
        'schedule': crontab(minute='*/3'),
    },
}
