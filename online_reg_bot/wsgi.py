"""
WSGI config for online_reg_bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from decouple import config
from django.core.wsgi import get_wsgi_application

DEBUG = config('DEBUG', cast=bool)
if DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'online_reg_bot.settings.dev')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'online_reg_bot.settings.prod')

application = get_wsgi_application()
