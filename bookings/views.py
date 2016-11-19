from datetime import datetime, timezone
from django.utils.dateparse import parse_date
from django.utils.dateparse import parse_time
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View
from pytimeparse.timeparse import timeparse

from bookings.models import Booking, Schedule, Record


def home(request):
    return render(request, "bookings/home.html")


def about(request):
    return render(request, "bookings/about.html")


def show_soundmans(request):
    group = Group.objects.get(name="Soundmans")
    soundmans = group.user_set.all()
    context = {
        'soundmans': soundmans
    }
    return render(request, "bookings/show_soundmans.html", context)


def show_calendar(request, soundman_id):
    return render(request, 'bookings/show_calendar.html')


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

        if date is not None:
            for schedule in schedules:
                if date.isoweekday() == schedule.working_day:
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
                'date': date,
                'today_schedule': today_schedule
            }

            return render(request, 'bookings/show_schedule.html', context)
        else:
            return render(request, 'accounts/http404.html')


def create_booking(request, soundman_id):
    args = {}
    args.update(csrf(request))
    new_booking = []
    soundman = get_object_or_404(User, id=soundman_id)
    if request.method == "POST":
        start = request.POST['start']
        end = request.POST['end']
        datestr = request.POST['date']
        date = parse_date(datestr)
        schedule = Schedule.objects.all().filter(soundman=soundman, working_day=date.isoweekday()).first()
        user = request.user
        bookings = Booking.objects.all().filter(date=date,schedule=schedule)   # Лист всех активных броней на текущую дату


        new_booking = Booking(user=user, start=start, end=end, is_active=1, date=date,
                              schedule=schedule)
        if parse_time(start) < schedule.start_of_the_day or parse_time(end) > schedule.end_of_the_day:
            # for books in bookings:
            # ToDo: Надо сделать проверку в цикле времен создаваемой брони с временами активных броней других пользователей
            new_booking = None
        else:
            new_booking.save()


        return render(request, 'bookings/show_result.html', {'new_booking': new_booking})


class CurrentRecordsView:
    def get(self):
        args = {}
        args.update(csrf(self))
        soundman = self.user
        try:
            args['bookings'] = Booking.objects.all().filter(schedule__soundman=soundman, date=datetime.now().date())
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
