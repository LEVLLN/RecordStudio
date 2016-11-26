from datetime import datetime, timezone, date, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.context_processors import csrf
from django.utils.dateparse import parse_date
from django.utils.dateparse import parse_time

from bookings.models import Booking, Schedule, Record


def home(request):
    return render(request, "bookings/home.html")


def about(request):
    return render(request, "bookings/about.html")


@login_required
def show_soundmans(request):
    context = {}
    group = Group.objects.get(name="Soundmans")
    soundmans = group.user_set.all()

    if request.user.groups.filter(name='Customers').exists():
        context = {
            'soundmans': soundmans
        }
        return render(request, "bookings/show_soundmans.html", context)
    else:
        context['error'] = "Вы не являетесь клиентом системы,вы не имеете права создавать бронь"
        return render(request, "bookings/show_soundmans.html", context)


@login_required
def show_calendar(request, soundman_id):
    return render(request, 'bookings/show_calendar.html')


@login_required
def show_schedule(request, soundman_id):
    args = {}
    context = {}
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
                            }
        if date < datetime.today().date():
            today_schedule = None
            context['error'] = "На предыдущую дату невозможно создать бронь"
            return render(request, 'bookings/show_calendar.html', context)
        if request.user.groups.filter(name='Customers').exists():
            context['today_schedule'] = today_schedule
            return render(request, 'bookings/show_calendar.html', context)
        elif not request.user.is_authenticated():
            return redirect("accounts/login")
        else:
            context['error'] = "Вы не являетесь клиентом системы,вы не имеете права создавать бронь"
            return render(request, 'bookings/show_calendar.html', context)


@login_required
def create_booking(request, soundman_id):
    args = {}
    args.update(csrf(request))
    context = {}
    new_booking = []
    soundman = get_object_or_404(User, id=soundman_id)
    if request.method == "POST":
        start = request.POST['start']
        end = request.POST['end']
        datestr = request.POST['date']
        date = parse_date(datestr)
        schedule = Schedule.objects.all().filter(soundman=soundman, working_day=date.isoweekday()).first()
        user = request.user
        bookings = Booking.objects.all().filter(date=date, schedule=schedule,
                                                is_active=1)  # Лист всех активных броней на текущую дату

        new_booking = Booking(user=user, start=start, end=end, is_active=1, date=date,
                              schedule=schedule)
        flag = False
        start_time = parse_time(start)
        deltastart = timedelta(hours=start_time.hour, minutes=start_time.minute)
        end_time = parse_time(end)
        deltaend = timedelta(hours=end_time.hour, minutes=end_time.minute)
        print("ДЕЛЬТА СТАРТ", deltastart)
        print("ДЕЛЬТА КОНЕЦ", deltaend)
        delta = deltaend - deltastart
        print("РАЗНИЦА ДЕЛЬТ", delta)

        for book in bookings:
            print(flag)
            if book.start <= parse_time(start) and book.end >= parse_time(end):
                flag = True
            if book.start >= parse_time(start) and book.end <= parse_time(end):
                flag = True
            if book.start <= parse_time(start) and book.end <= parse_time(end) and book.end >= parse_time(start):
                flag = True
            if book.start >= parse_time(start) and book.end >= parse_time(end) and book.start <= parse_time(end):
                flag = True

    if parse_time(start) < schedule.start_of_the_day or parse_time(end) > schedule.end_of_the_day or parse_time(
            start) > schedule.end_of_the_day or parse_time(end) < schedule.start_of_the_day:
        # for books in bookings:
        # ToDo: Надо сделать проверку в цикле времен создаваемой брони с временами активных броней других пользователей
        context['error'] = "Вы выбрали время, не совпадающее с временем работы звукорежиссера"
        print(bookings)
        return render(request, 'bookings/show_calendar.html', context)

    elif parse_time(start) >= parse_time(end):
        context['error'] = "Начало записи не может быть больше или равно концу записи"
        return render(request, 'bookings/show_calendar.html', context)
    elif flag:
        context['error'] = "На это время имеются брони"
        print(book)
        return render(request, 'bookings/show_calendar.html', context)
    elif delta < timedelta(minutes=30):
        context['error'] = "Минимальная подолжительность записи 30 минут"
        return render(request, 'bookings/show_calendar.html', context)

    else:
        new_booking.save()
        context['new_booking'] = new_booking
        context['duration'] = delta
        return render(request, 'bookings/show_calendar.html', context)


@login_required
class RecordView:
    def details(self, booking_id):
        return render(self, "records/user_record_page.html")

    def start_record_method(self, booking_id):
        if self.POST:
            args = {}
            args.update(csrf(self))
            # reservationId = request.POST['id']
            try:
                # Если статус брони = "отменен" / "завершен" то выбросит ошибку
                if Booking.objects.get(pk=booking_id).is_active == 3 or \
                                Booking.objects.get(pk=booking_id).is_active == 4:
                    args['againClicked'] = "Record is canceled or inactive"
                    return render(self, "records/user_record_page.html", args)

                # Если начало записи уже есть в БД то выбросит сообщение, что запись уже начата
                if not Record.objects.get(reservation_id=booking_id).start_record is None:
                    args['againClicked'] = "Record is already started"
                    return render(self, "records/user_record_page.html", args)

                # Проверка опоздал ли пользоватеь или нет
                if (datetime.now(timezone.utc) - Booking.objects.get(pk=booking_id).start) > timedelta(minutes=15):
                    args['mal'] = "The user is kotakbas"
                    return render(self, "records/user_record_page.html", args)

            except ObjectDoesNotExist:
                # Проверка опоздал ли пользоватеь или нет
                if datetime.combine(date.min, datetime.now().time()) - datetime.combine(date.min, Booking.objects.get(
                        pk=booking_id).start) > timedelta(minutes=15):
                    args['mal'] = "The user is kotakbas"
                    return render(self, "records/user_record_page.html", args)

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

            # Если время окончание записи пуста
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

            # Если статус брони = "отменен" / "завершен" то выбросит ошибку
            if Booking.objects.get(pk=booking_id).is_active == 3 or \
                            Booking.objects.get(pk=booking_id).is_active == 4:
                args['againStopped'] = "Record is canceled or inactive"
                return render(self, "records/user_record_page.html", args)

            args['againStopped'] = "Record is already stopped"
            return render(self, "records/user_record_page.html", args)

        return redirect('/accounts/my_profile')


def cancel_booking(request, booking_id):
    booking_object = Booking.objects.get(id=booking_id)
    booking_object.is_active = 4
    booking_object.save()
    return redirect('/accounts/my_profile')
