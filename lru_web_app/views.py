from django.shortcuts import render
from django.core.paginator import Paginator
from lru_web_app.models import Person
from .my_lru import LRUCache


@LRUCache
def find_person(name, city):
    """ This is a remarkably slow and stupid way to look for a person. However the LRU-cache will cache people after they have been found, speeding up the process once the person is looked up again. """
    for person in Person.objects.all():
        if person.name == name and person.city == city:
            return person


def home(request):
    paginator = Paginator(Person.objects.all(), 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})


def person_page(request, name, city):
    person = find_person(name, city)
    return render(request, "person_page.html", {"person":person})
