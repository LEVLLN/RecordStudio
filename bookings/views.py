from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


@login_required()
def home(request):
    return render(request, 'bookings/home.html')


def test(request):
    return HttpResponse(request, "fdsfdsfs")


def booking(request):
    template = "booking/book.html"
    return HttpResponse(request, template)
