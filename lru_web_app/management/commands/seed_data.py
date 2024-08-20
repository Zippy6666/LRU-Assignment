from django.core.management.base import BaseCommand
from lru_web_app.models import Person
from faker import Faker

SEED_DATA_COUNT:int = 20_000


def to_person_number(num: int) -> str:
    num = str(num)
    personnummer = f"{num[0:8]}-{num[8:12]}"
    return personnummer


class Command(BaseCommand):
    help = "Seeds data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE(f"Trying to seed data... {args} {kwargs}"))

        Person.objects.all().delete()
        self.stdout.write(self.style.NOTICE('Removed any old "Person" instances...'))

        fake = Faker()
        objects = []
        self.stdout.write(self.style.NOTICE("Instanciating objects, please wait..."))
        for _ in range(SEED_DATA_COUNT):
            city = fake.city()
            person_number = to_person_number(
                fake.random_number(digits=12, fix_len=True)
            )
            name = fake.name()
            job = fake.job()
            country = fake.country()
            phone_number = fake.phone_number()
            person = Person(
                name=name,
                job=job,
                country=country,
                phone_number=phone_number,
                person_number=person_number,
                city=city,
            )
            objects.append(person)

        self.stdout.write(self.style.NOTICE("Bulk creating objects, please wait..."))
        if objects:
            Person.objects.bulk_create(objects, batch_size=10_000)

        first_person = Person.objects.first()
        name = first_person.name
        person_number = first_person.person_number
        phone_number = first_person.phone_number
        self.stdout.write(
            self.style.SUCCESS(
                f"Sucess! Example person: {name} {person_number} {phone_number}"
            )
        )
