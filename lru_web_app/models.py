from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    person_number = models.CharField(max_length=12)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    job = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
