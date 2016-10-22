from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf


def login(request):
    args = {}
    args.update(csrf(request))
    if request.method == "GET":
        if request.user.is_authenticated():
            return HttpResponse("You are already authorized")
        else:
            return render(request, "accounts/login.html")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect("/")
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response("accounts/login.html", args)


def logout(request):
    auth.logout(request)
    return redirect("/accounts/login/")


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        new_user_form = UserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'],
                                         password=new_user_form.cleaned_data['password2'])
            auth.login(request, new_user)
            return redirect('/')
        else:
            args['form'] = new_user_form
    return render_to_response('accounts/register.html', args)
