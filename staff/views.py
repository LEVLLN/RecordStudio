from datetime import datetime

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, User
from django.http import Http404
from django.shortcuts import render, redirect, render_to_response

# _______________________
# staff stuff
# _______________________


# Staff's login page
# url : /staff
from django.template.context_processors import csrf
from django.views import View

from accounts.forms import UserCreationForm, SoundmanCreationForm
from accounts.views import ForgetPasswordView
from bookings.models import Record, Booking
from emailer.views import send_email


class StaffLoginPageView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('/staff/profile')
        return render(request, 'staff/loginPage.html')

    def post(self, request):
        args = {}
        args.update(csrf(request))
        user = authenticate(username=request.POST['login'].lower(),
                            password=request.POST['password'])
        if user is not None and user.is_active:
            if user.groups.filter(name='Administrators').exists() or \
                    user.groups.filter(name='Soundmans').exists():
                auth.login(request, user)
                return redirect('/staff/profile')
            raise Http404()
        else:
            args['login_error'] = "Ошибка авторизации"
            return render(request, "staff/loginPage.html", args)


# url: /profile
class StaffProfilePageView(View):
    def get(self, request):
        if request.user.is_authenticated():
            if request.user.groups.filter(name='Administrators').exists():
                context = {
                    "Records": Record.objects.all(),
                    "allBookings": Booking.objects.all().order_by('date')
                }
                return render(request, 'staff/administrators_page.html', context)
            elif request.user.groups.filter(name='Soundmans').exists():
                context = {
                    "bookings": Booking.objects.filter(schedule__soundman=request.user).order_by('date'),
                }
                return render(request, 'staff/soundmans_page.html', context)
        raise Http404()

    def post(self, request):
        user_id = User.objects.get(username=request.user).id
        # Чекает 1) Пришла ли дата методом пост; 2) Пришла ли дата правильно
        try:
            date = request.POST['date']
            datetime.strptime(date, '%Y-%m-%d')
        except Exception:  # Если дата приходит в неверном формате, то вручную указываем дату сегоднящнего дня
            date = datetime.now().date()
        if request.user.groups.filter(name='Soundmans').exists():
            context = {
                "bookings": Booking.objects.filter(schedule__soundman=user_id, date=date).order_by('date'),
            }
            return render(request, 'staff/soundmans_page.html', context)
        elif request.user.groups.filter(name='Administrators').exists():
            context = {
                "Records": Record.objects.all(),
                "allBookings": Booking.objects.filter(date=date).order_by('date')
            }
            return render(request, 'staff/administrators_page.html', context)
        raise Http404()


class SoundmanAddView(View):
    def get(self, request):
        if request.user.groups.filter(name='Administrators').exists():
            return render(request, 'staff/soundmanAdd.html')
        raise Http404()

    def post(self, request):
        if ('first_name' and 'last_name' and 'login' and 'email') in request.POST:
            args = {}
            args.update(csrf(request))
            new_user_form = SoundmanCreationForm(request.POST)
            if new_user_form.is_valid():
                new_user = User.objects.create_user(username=new_user_form.cleaned_data['username'].lower(),
                                                    first_name=new_user_form.cleaned_data['first_name'],
                                                    last_name=new_user_form.cleaned_data['last_name'],
                                                    email=new_user_form.cleaned_data['email'],
                                                    )
                password = ForgetPasswordView()
                __new_password_of_soundman = password.password_generating_method()
                new_user.set_password(__new_password_of_soundman)
                new_user.is_active = True
                new_user.save()
                Group.objects.get(name='Soundmans').user_set.add(new_user)

                return send_email(email=request.POST['email'],
                                  username=request.POST['login'],
                                  password=__new_password_of_soundman,
                                  first_name=request.POST['first_name'],
                                  last_name=request.POST['last_name'])

            args['form'] = new_user_form
            return render_to_response('staff/soundmanAdd.html', args)
        raise Http404()

