from django.core.management.base import BaseCommand
from django.core.management import call_command
from lru_web_app.models import Person
from faker import Faker


SEED_DATA_COUNT: int = 1_000_000
BATCH_SIZE: int = SEED_DATA_COUNT // 100


def to_pn(num: int) -> str:
    num = str(num)
    pn = f"{num[0:8]}-{num[8:12]}"
    return pn


class Command(BaseCommand):
    help = "Seeds people into the database."

    def _seed_people(self) -> Person:
        """ Seeds people into the database. Returns the first generated person """

        call_command("clear_people")

        fake = Faker()
        objects = []
        bulk_creations = 0
        self.stdout.write(self.style.NOTICE("Instanciating objects, please wait..."))
        for _ in range(SEED_DATA_COUNT):
            city = fake.city()
            pn = to_pn(fake.random_number(digits=12, fix_len=True))
            name = fake.name()
            job = fake.job()
            country = fake.country()
            phone_number = fake.phone_number()
            person = Person(
                name=name,
                job=job,
                country=country,
                phone_number=phone_number,
                pn=pn,
                city=city,
            )
            objects.append(person)

            if len(objects) >= BATCH_SIZE:
                Person.objects.bulk_create(objects)
                objects.clear()
                bulk_creations += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{bulk_creations}/{SEED_DATA_COUNT//BATCH_SIZE} batches done!"
                    )
                )

        # Handle remaining objects if any are left after the loop
        if objects:
            Person.objects.bulk_create(objects)
            self.stdout.write(self.style.SUCCESS("Final batch done!"))

        return Person.objects.first()


    def handle(self, *_, **__):
        self.stdout.write(self.style.NOTICE("Going to seed data, proceed? (y/n)"))
        if input().lower() != "y":
            return
        
        try:
            first_person = self._seed_people()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Exception thrown: {type(e)} {e}"))
        else:
            first_name = first_person.name
            first_pn = first_person.pn
            first_phone_number = first_person.phone_number
            self.stdout.write(
                self.style.SUCCESS(
                    f"Sucess! Example person: {first_name}, pn: {first_pn}, phone number: {first_phone_number}"
                )
            )
