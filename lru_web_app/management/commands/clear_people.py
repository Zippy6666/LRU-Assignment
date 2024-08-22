from django.core.management.base import BaseCommand
from lru_web_app.models import Person

class Command(BaseCommand):
    help = "Removes all people from the database."

    def handle(self, *_, **__):
        self.stdout.write(self.style.NOTICE("Removing all people..."))
        Person.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("People removed!"))
