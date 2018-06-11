#!/usr/bin/env python
import os
import bjoern
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()

bjoern.run(
    wsgi_app=application,
    host='0.0.0.0',
    port=9808,
    reuse_port=True
)
