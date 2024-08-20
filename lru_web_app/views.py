from django.shortcuts import render
from django.core.paginator import Paginator
from lru_web_app.models import Person


def home(request):
    paginator = Paginator(Person.objects.all(), 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "home.html", {"page_obj": page_obj})


def person_page(request):
    return render(request, "person_page.html")
