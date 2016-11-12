from datetime import datetime, timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View
from pytimeparse.timeparse import timeparse

from bookings.models import Booking, Schedule, Record


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
        new_booking = Booking(user=user, start=start, is_active=1,
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


def show_schedule(request, soundman_id):
    args = {}
    args.update(csrf(request))
    soundman = get_object_or_404(User, id=soundman_id)
    schedules = Schedule.objects.all().filter(soundman=soundman)
    if request.method == "POST":
        bookings = Booking.objects.all().filter(schedule__soundman=soundman)
        datestr = request.POST['date']
        print(datestr)
        act_bookings = []
        today_schedule = []
        date = parse_date(datestr)
        print(date)
        for schedule in schedules:
            if date.isoweekday()==schedule.working_day:
                print(schedule)
                today_schedule.append(schedule)
            for booking in bookings:
                if schedule == booking.schedule:
                    if booking.is_active == 1:
                        if booking.date == date:
                            print("имеется бронь на эту дату")
                            act_bookings.append(booking)
        context = {
            'soundman': soundman,
            'schedules': schedules,
            'bookings': bookings,
            'active_bookings': act_bookings,
            'date':date,
            'today_schedule': today_schedule
        }
        return render(request, 'bookings/show_schedule.html', context)
    elif request.method == "GET":
        context = {
            'schedule': schedules
        }
        return render(request, 'bookings/show_calendar.html', context)


# def show_soundman_schedule(request, soundman_id):
#  soundman = get_object_or_404(User, id=soundman_id)
#     print(soundman)
#     schedules = Schedule.objects.all().filter(soundman=soundman)
#     print(schedules)
#     bookings = Booking.objects.all().filter(soundman=soundman)
#     context = {
#         'schedules': schedules,
#         'bookings': bookings
#     }
#     for sch in schedules:
#         deltaStart = timedelta(hours=sch.start_of_the_day.hour, minutes=sch.start_of_the_day.minute)
#         deltaEnd = timedelta(hours=sch.end_of_the_day.hour, minutes=sch.end_of_the_day.minute)
#         delta = deltaEnd - deltaStart
#         slotscount = (delta.seconds / 3600) / 2
#         slotstimeStart = deltaStart
#         # for i in slotscount:
#         #     slotstimeEnd = slotstimeStart+2
#         #     slotsStart.insert(slotstimeStart)
#         #     print(slotstimeStart)
#         k = int(slotscount)
#         i = 0
#         slots = []
#         starEndslots = []
#         print("Начало расписания:",sch.start_of_the_day)
#         print("Конец расписания:", sch.end_of_the_day)
#         print("Всего слотов на это расписание:", k)
#         while i < k:
#             i = i + 1
#             print("Слот номер:",i)
#             print("Начало времени слота:",slotstimeStart)
#             slotstimeEnd = slotstimeStart + timedelta(hours=2)
#             print("Конец времени слота:",slotstimeEnd)
#             starEndslots = [(slotstimeStart.seconds/3600), slotstimeEnd.seconds/3600]
#             slots.insert(i, starEndslots)
#             slotstimeStart = slotstimeEnd
#             # print(slotstimeStart)
#             # slottimeEnd = slotstimeStart+2
#             # slotstimeStart = slottimeEnd
#             # print(slottimeEnd)
#
#             # check git cmd changes
#         print("непонятный список слотов:",slots)
#     return render(request, "bookings/show_schedule.html", context)

class CurrentRecordsView:
    def get(self):
        args = {}
        args.update(csrf(self))
        soundman = self.user
        try:
            args['bookings'] = Booking.objects.all().filter(schedule__soundman=soundman)
            return render_to_response('records/current_records.html', args)
        except ObjectDoesNotExist:
            args['nobookings'] = "You have no customers who booked"
            return render_to_response('records/current_records.html', args)


class RecordView:
    def details(self, booking_id):
        return render(self, "records/user_record_page.html")

    def start_record_method(self, booking_id):
        if self.POST:
            args = {}
            args.update(csrf(self))
            # reservationId = request.POST['id']
            try:

                if not Record.objects.get(reservation_id=booking_id).start_record is None:
                    args['againClicked'] = "Record is already started"
                    return render(self, "records/user_record_page.html", args)

            except ObjectDoesNotExist:
                _new_record = Record(reservation_id=booking_id, start_record=datetime.now(timezone.utc))
                _new_record.save()

                _reservation = Booking.objects.get(pk=booking_id)
                _reservation.is_active = 2
                _reservation.save()
                args['againClicked'] = "Record is starting"
                return render(self, "records/user_record_page.html", args)

        return redirect('/accounts/my_profile')

    def stop_record_method(self, booking_id):
        if self.POST:
            args = {}
            args.update(csrf(self))

            if Record.objects.get(reservation_id=booking_id).stop_record is None:
                _new_record = Record.objects.get(reservation_id=booking_id)
                _new_record.stop_record = datetime.now(timezone.utc)

                # duration is in minutes
                duration = (_new_record.stop_record - _new_record.start_record).seconds / 60
                price_per_minute = 100  # The price per minute of record

                if duration > 5:
                    _new_record.money_back = duration * price_per_minute
                else:
                    _new_record.money_back = 0

                _new_record.save()

                _reservation = Booking.objects.get(pk=booking_id)
                _reservation.is_active = 3
                _reservation.save()

                args['againStopped'] = "Record is stopping"
                return render(self, "records/user_record_page.html", args)

            args['againStopped'] = "Record is already stopped"
            return render(self, "records/user_record_page.html", args)

        return redirect('/accounts/my_profile')
