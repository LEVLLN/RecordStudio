from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
from bookings.models import Reservation
import datetime

def home(request):
    return render(request, 'bookings/home.html')

def create_booking(request):
    reserv = Reservation.objects.all()
    context = {
        'bookings':reserv
    }
    user = auth.authenticate(username='admin',password='qwertY123')
    auth.login(request,user)
    new_booking = Reservation(user=user,start='2016-01-31 15:00',is_active=1,duration=datetime.timedelta(hours=1, minutes=60,seconds=12),soundman=user)
    new_booking.save()
    return render(request, 'bookings/create_booking.html', context)
