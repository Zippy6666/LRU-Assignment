"""
WSGI config for lru_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from lru_web_app.models import Person
from lru_web_app.management.commands.seed_people import SEED_DATA_COUNT


# Migrate any database changes
call_command("migrate")


# Seed data
if Person.objects.count() != SEED_DATA_COUNT:
    call_command("seed_people")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lru_project.settings")
application = get_wsgi_application()
