from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf


def login(request):
    args = {}
    args.update(csrf(request))

    if request.method == "GET":

        if request.user.is_authenticated():

            if request.user.groups.filter(name='Administrators').exists():
                return render(request, "administrator/administrator_page.html")
            if request.user.groups.filter(name='Soundman').exists():
                return render(request, "soundman_p/soundman_page.html")
            else:
                return redirect("/")

        else:
            return render(request, "accounts/login.html")

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)

            if request.user.groups.filter(name='Administrators').exists():
                return render(request, "administrator/administrator_page.html")
            if request.user.groups.filter(name='Soundman').exists():
                return render(request, "soundman_p/soundman_page.html")
            else:
                return redirect("/")

        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response("accounts/login.html", args)

    else:
        return HttpResponse(request, "accounts/login.html")


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
                new_user_form.save()
                email = request.POST['email']
                new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                             password=new_user_form.cleaned_data['password2'],
                                             email=email)
                auth.login(request, new_user)
                return redirect(request)
            else:
                args['form'] = new_user_form
                return render_to_response('accounts/register.html', args)

    return render(request, 'bookings/home.html')


@user_passes_test(lambda u: u.groups.filter(name='soundmans').exists())
def soundman_page(request):
    return render(request, "soundman_p/soundman_page.html")


@user_passes_test(lambda u: u.groups.filter(name='Administrators').exists())
def administrators_page(request):
    return render(request, "administrator/administrator_page.html")
