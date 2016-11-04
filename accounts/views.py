import random
import string

from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View

from accounts.forms import UserCreationForm
from emailer.views import send_welcome_mail, send_forget_mail


class ForgetPasswordView(View):
    @staticmethod
    def get(request):
        return render(request, 'accounts/forget.html')

    def post(self, request):
        args = {}
        args.update(csrf(request))
        try:
            validate_email(request.POST['email'])
            email = request.POST['email']
            try:
                user = User.objects.get(email=email)
                __new_password = self.passGeneratorMethod()
                user.set_password(__new_password)
                return send_forget_mail(email, user.username, __new_password)  #
            except ObjectDoesNotExist:
                args['NoUserFound'] = "Почтовый ящик или логин не найдены."
                return render_to_response("accounts/forget.html", args)

        except ValidationError:
            username = request.POST['email']  # реализовать удаление пробелов
            try:
                user = User.objects.get(username=username)
                email = user.email
                __new_password = self.passGeneratorMethod()
                user.set_password(__new_password)
                return send_forget_mail(email, username, __new_password)
            except ObjectDoesNotExist:
                args['NoUserFound'] = "Почтовый ящик или логин не найдены."
                return render_to_response("accounts/forget.html", args)

    @staticmethod
    def passGeneratorMethod(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


class AuthenticationView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return self.check_for_permission(request)
        else:
            return render(request, "accounts/login.html")

    def post(self, request):
        args = {}
        args.update(csrf(request))
        user = authenticate(username=request.POST['username'].lower(),
                            password=request.POST['password'])

        if user is not None and user.is_active:
            auth.login(request, user)
            return self.check_for_permission(request)
        else:
            args['login_error'] = "Ошибка авторизации"
            return render_to_response("accounts/login.html", args)

    @staticmethod
    def logout(request):
        auth.logout(request)
        return redirect("/accounts/login/")

    @staticmethod
    def check_for_permission(request):
        if request.user.groups.filter(name='Administrators').exists():
            return render(request, "administrator/administrator_page.html")
        if request.user.groups.filter(name='Soundmans').exists():
            return render(request, "soundman_p/soundman_page.html")
        if request.user.groups.filter(name='Customers').exists():
            return render(request, "user/home.html")
        else:
            return redirect('/')


class RegistrationView(View):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated():
            return render(request, 'accounts/register.html')
        return render(request, 'bookings/home.html')

    @staticmethod
    def post(request):
        if not request.user.is_authenticated():
            args = {}
            args.update(csrf(request))
            args['form'] = UserCreationForm()
            new_user_form = UserCreationForm(request.POST)
            if new_user_form.is_valid():
                new_user = User(username=new_user_form.cleaned_data['username'].lower(),
                                password=new_user_form.cleaned_data['password2'],
                                email=new_user_form.cleaned_data['email'],
                                first_name=new_user_form.cleaned_data['first_name'],
                                last_name=new_user_form.cleaned_data['last_name'])

                new_user.set_password(new_user_form.cleaned_data["password2"])  # хеширует пароль :С
                new_user.save()
                Group.objects.get(name='Customers').user_set.add(new_user)
                auth.login(request, new_user)
                return send_welcome_mail(new_user_form.cleaned_data['username'].lower(),
                                         new_user_form.cleaned_data['password2'],
                                         new_user_form.cleaned_data['email'],
                                         new_user_form.cleaned_data['first_name'],
                                         new_user_form.cleaned_data['last_name'])
            else:
                args['form'] = new_user_form
                return render_to_response('accounts/register.html', args)

        return render(request, 'bookings/home.html')

