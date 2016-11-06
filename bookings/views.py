from datetime import datetime, timezone, timedelta

from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template.context_processors import csrf
from pytimeparse.timeparse import timeparse

from bookings.models import Reservation, Schedule, Record


# def home(request):
#     # soundman = User.objects.filter(groups='soundman')
#
#     group = Group.objects.get(name='soundmans')
#     users = group.user_set.all()
#     context = {
#         'sounmanlist': users
#     }
#     print(users)
#     return render(request, 'bookings/create_booking.html', context)
#

# def create_booking(request):
#     duration = request.POST['duration']
#     start = request.POST['start']
#     soundman = request.POST['soundman']
#     print(start)
#     print(soundman)
#
#     user = request.user
#     new_booking = Reservation(user=user, start=start, is_active=1,
#                               duration=datetime.timedelta(minutes=timeparse(duration)),
#                               soundman=request.user)
#     new_booking.save()
#     reserv = Reservation.objects.all()
#     context = {
#         'bookings': new_booking
#     }
#     return render(request, 'bookings/show_booking.html', context)


# ___________________________________________________________________________________________
def creating_booking(request):
    args = {}
    args.update(csrf(request))
    if request.method == "GET":
        group = Group.objects.get(name='Soundmans')
        users = group.user_set.all()
        context = {
            'sounmanlist': users
        }
        print(users)
        return render(request, 'bookings/create_booking.html', context)
    elif request.method == "POST":
        duration = request.POST['duration']
        start = request.POST['start']
        soundman_str = request.POST['soundman']
        soundman = User.objects.get(username=soundman_str)
        user = request.user
        new_booking = Reservation(user=user, start=start, is_active=1,
                                  duration=datetime.timedelta(minutes=timeparse(duration)),
                                  soundman=soundman)
        if request.user.groups.filter(name='Customers').exists():
            new_booking.save()
            return render(request, 'bookings/show_booking.html', {'booking': new_booking})
        else:
            return HttpResponse('U cant do this')


def home(request):
        return render(request, "bookings/home.html")

def about(request):
        return render(request, "bookings/about.html")
        
# _________________________________________________________________________________________
#
def show_soundmans(request):
    group = Group.objects.get(name="Soundmans")
    soundmans = group.user_set.all()
    context = {
        'soundmans': soundmans
    }
    return render(request, "bookings/show_soundmans.html", context)


def show_soundman_schedule(request, soundman_id):

    soundman = get_object_or_404(User, id=soundman_id)
    print(soundman)
    schedules = Schedule.objects.all().filter(soundman=soundman)
    print(schedules)
    bookings = Reservation.objects.all().filter(soundman=soundman)
    context = {
        'schedules': schedules,
        'bookings': bookings
    }
    for sch in schedules:
        deltaStart = timedelta(hours=sch.start_of_the_day.hour, minutes=sch.start_of_the_day.minute)
        deltaEnd = timedelta(hours=sch.end_of_the_day.hour, minutes=sch.end_of_the_day.minute)
        delta = deltaEnd-deltaStart
        slotscount = (delta.seconds/3600)/2
        print("SLOTS:",slotscount)
        #check git cmd changes
    return render(request, "bookings/show_soundman_schedule.html", context)



class RecordView:
    def start_record(request):
        if request.POST:
            new_record = Record(reservation_id=72, start_record=datetime.now(timezone.utc))
            new_record.save()
            return redirect("/accounts/my_profile")
        else:
            return render(request, "records/records.html")

    def stop_record(request):
        if request.POST:
            new_record = Record.objects.get(reservation_id=72)
            stop_record = datetime.now(timezone.utc)
            new_record.stop_record = stop_record
            dur = stop_record - new_record.start_record
            new_record.current_duration = dur.seconds/60
            new_record.save()
            return redirect("/accounts/my_profile")
        else:
            return render(request, "records/records.html")
