from delivery_service.celery import app

from .services import auto_update_tracks_location


@app.task
def update_trucks():
    auto_update_tracks_location()
