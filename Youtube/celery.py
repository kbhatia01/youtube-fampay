import logging
import os

from celery import Celery
from django.conf import settings

# Get an instance of a logger
logger = logging.getLogger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Youtube.settings')

app = Celery('Youtube')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(packages=settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'fetch_data': {
        'task': 'Search.tasks.fetch_data',
        'schedule': 10.0
    }
}


@app.task(bind=True)
def debug_task(self):
    logger.error(f'Request: {self.request!r}')
