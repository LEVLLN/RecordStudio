from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from bookings.models import Reservation
import datetime
from pytimeparse.timeparse import timeparse

def home(request):
    return render(request, 'bookings/home.html')

def create_booking(request):


    duration = request.POST['duration']
    start = request.POST['start']

    print(start)
    print(duration)

    user = request.user
    new_booking = Reservation(user=user, start=start, is_active=1, duration=datetime.timedelta(minutes=timeparse(duration)), soundman=user)
    new_booking.save()
    reserv = Reservation.objects.all()
    context = {
        'bookings': new_booking
    }
    return render(request, 'bookings/create_booking.html', context)
