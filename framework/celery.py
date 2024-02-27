from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'framework.settings')

app = Celery('framework')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.broker_connection_retry_on_startup = True


app.conf.beat_schedule = {
    "ingest_data": {
        "task": "loan.tasks.ingest_data",
        "schedule": crontab(minute='*', hour='*', day_of_week='*'),
    },
}

if __name__ == '__main__':
    app.worker_main()