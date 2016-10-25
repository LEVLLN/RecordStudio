import random
import re
import string

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf

from accounts.forms import UserCreationForm
from emailer.views import send_welcome_mail, send_forget_mail


def check_for_permission(request):
    if request.user.groups.filter(name='Administrators').exists():
        return render(request, "administrator/administrator_page.html")
    if request.user.groups.filter(name='Soundman').exists():
        return render(request, "soundman_p/soundman_page.html")
    # прописать чек для кастомера
    else:
        return render(request, "user/home.html")


def login(request):
    args = {}
    args.update(csrf(request))

    if request.user.is_authenticated():
        return check_for_permission(request)
    else:
        if request.method == "GET":
            return render(request, "accounts/login.html")

        else:
            user = authenticate(username=request.POST['username'].lower(),
                                password=request.POST['password'])

            if user is not None and user.is_active:
                auth.login(request, user)
                return check_for_permission(request)
            else:
                args['login_error'] = "Ошибка авторизации"
                return render_to_response("accounts/login.html", args)


def logout(request):
    auth.logout(request)
    return redirect("/accounts/login/")


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()

    if not request.user.is_authenticated():
        if request.POST:
            new_user_form = UserCreationForm(request.POST)
            if new_user_form.is_valid():
                new_user = User(username=new_user_form.cleaned_data['username'].lower(), # Реализовать удаление пробелов
                                password=new_user_form.cleaned_data['password2'],
                                email=new_user_form.cleaned_data['email'],
                                first_name=new_user_form.cleaned_data['first_name'],
                                last_name=new_user_form.cleaned_data['last_name'])

                new_user.save()

                # Добавить пользователя в группу кастомерс

                send_welcome_mail(new_user_form.cleaned_data['username'].lower(),
                                  new_user_form.cleaned_data['password2'],
                                  new_user_form.cleaned_data['email'], new_user_form.cleaned_data['first_name'],
                                  new_user_form.cleaned_data['last_name'])
                auth.login(request, new_user)
                return redirect("/")

            else:
                args['form'] = new_user_form
                return render_to_response('accounts/register.html', args)

        else:
            return render(request, 'accounts/register.html')

    else:
        return render(request, 'bookings/home.html')


def forget(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'GET':
        return render(request, 'accounts/forget.html')
    else:
        result = re.search(r"@", request.POST['email'])
        if result:
            email = request.POST['email']
            user = User.objects.get(email=email)
            __new_password = pass_generator()
            user.set_password(__new_password)
            send_forget_mail(email, user.username, __new_password)
            # Реализовать озвращение на страницу success или возвращение сообщения об успешной отправки мыла
            return redirect('/')
        else:
            username = request.POST['email'] # реализовать удаление пробелов
            user = User.objects.get(username=username)
            email = user.email
            __new_password = pass_generator()
            send_forget_mail(email, username, __new_password)
            return redirect('/')


def pass_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
