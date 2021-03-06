from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('challenge', broker='amqp://' + os.environ['RABBITMQ_DEFAULT_USER'] + ':' + os.environ['RABBITMQ_DEFAULT_PASS'] + '@rabbitmq:5672/my_vhost')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

