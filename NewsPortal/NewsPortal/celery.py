import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal ')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_week_notification': {
        'task': 'News.tasks.posts_weekly_notification',
        'schedule': crontab(hour=8, minute=00, day_of_week='monday'),
     }
}


