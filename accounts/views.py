from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf


def check_for_permission(request):
    if request.user.groups.filter(name='Administrators').exists():
        return render(request, "administrator/administrator_page.html")
    if request.user.groups.filter(name='Soundman').exists():
        return render(request, "soundman_p/soundman_page.html")
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
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

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

                username = new_user_form.cleaned_data['username']
                password = new_user_form.cleaned_data['password2']
                email = request.POST['email']

                new_user = User(username=username, password=password, email=email)
                new_user.save()
                auth.login(request, new_user)
                return redirect("/")

            else:
                args['form'] = new_user_form
                return render_to_response('accounts/register.html', args)

        else:
            return render(request, 'accounts/register.html')

    else:
        return render(request, 'bookings/home.html')
