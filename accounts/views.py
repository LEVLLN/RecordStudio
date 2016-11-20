import random
import string
from datetime import datetime, timezone, timedelta

from django.contrib import auth
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views import View
from django.http import Http404

from accounts.forms import UserCreationForm
from accounts.models import SecretHashCode
from emailer.views import send_email


class ForgetPasswordView(View):
    @staticmethod
    def get(request):
        if not request.user.is_authenticated():
            return render(request, 'accounts/forget.html')
        return render(request, 'accounts/http404.html')

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
                return send_email(email=email, username=user.username, password=__new_password)

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
                return send_email(email=email, username=user.username, password=__new_password)
            except ObjectDoesNotExist:
                args['NoUserFound'] = "Почтовый ящик или логин не найдены."
                return render_to_response("accounts/forget.html", args)

    @staticmethod
    def passGeneratorMethod(size=8, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))


class AuthenticationView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated():
            return render(request, 'accounts/http404.html')
        return render(request, "accounts/login.html")

    @staticmethod
    def post(request):
        args = {}
        args.update(csrf(request))
        user = authenticate(username=request.POST['username'].lower(),
                            password=request.POST['password'])

        if user is not None and user.is_active:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Ошибка авторизации"
            return render_to_response("accounts/login.html", args)

    @staticmethod
    def logout(request):
        auth.logout(request)
        return redirect("/")

    @staticmethod
    def check_for_permission(request):
        if request.user.groups.filter(name='Administrators').exists():
            return render(request, "administrator/administrator_page.html")
        if request.user.groups.filter(name='Soundmans').exists():
            return render(request, "soundman/soundman_page.html")
        if request.user.groups.filter(name='Customers').exists():
            return render(request, "user/profile.html")
        return redirect('/accounts/login')


class RegistrationView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated():
            return render(request, 'accounts/http404.html')
        return render(request, 'accounts/register.html')

    @staticmethod
    def post(request):
        if not request.user.is_authenticated():
            args = {}
            args.update(csrf(request))
            args['form'] = UserCreationForm()
            new_user_form = UserCreationForm(request.POST)
            if new_user_form.is_valid():
                new_user = User.objects.create_user(username=new_user_form.cleaned_data['username'].lower(),
                                                    first_name=new_user_form.cleaned_data['first_name'],
                                                    last_name=new_user_form.cleaned_data['last_name'],
                                                    email=new_user_form.cleaned_data['email'],
                                                    )

                new_user.set_password(new_user_form.cleaned_data["password2"])  # хеширует пароль :С
                new_user.is_active = False
                new_user.save()
                Group.objects.get(name='Customers').user_set.add(new_user)

                SecretHashCode(user_id=new_user.pk,
                               hashcode=''.join(
                                   random.choice(string.ascii_uppercase + string.digits) for _ in range(12)),
                               expired_date=datetime.now(timezone.utc) + timedelta(minutes=60)
                               ).save()

                # auth.login(request, new_user)
                __new_hash = SecretHashCode.objects.get(user_id=new_user.pk).hashcode
                return send_email(email=new_user_form.cleaned_data['email'],
                                  username=new_user_form.cleaned_data['username'].lower(),
                                  password=new_user_form.cleaned_data['password2'],
                                  first_name=new_user_form.cleaned_data['first_name'],
                                  last_name=new_user_form.cleaned_data['last_name'],
                                  hash_code=__new_hash)
            else:
                args['form'] = new_user_form
                return render_to_response('accounts/register.html', args)

        return render(request, 'accounts/register.html')


class ConfirmView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated():
            raise Http404()

        # Пример ссылки для подтверждения
        # http://127.0.0.1:8000/accounts/confirm?username=hashtest&hash=VAYN76N0VUUQ

        args = {}
        args.update(csrf(request))
        username = request.GET['username']
        hash_code = request.GET['hash']
        try:
            user = User.objects.get(username=username)
            hash_of_user = SecretHashCode.objects.get(user_id=user.pk).hashcode
            expired_date = SecretHashCode.objects.get(user_id=user.pk).expired_date

            if datetime.now(timezone.utc) > expired_date:
                args['expired'] = "This Link is expired"
                args['username'] = username
                return render_to_response('accounts/confirm.html', args)

            # Выбросит ошибку, если хеш код не совпадает хешу пользователя
            if not hash_of_user == hash_code:  # В конце кадой ссылки идет слеш "/", который мешает проверке
                args['fail'] = "No hash code like this"
                return render_to_response('accounts/confirm.html', args)

            # Если пользователь уже активирован, то снова выбросит ошибку
            if user.is_active:
                args['alreadydone'] = "You have already confirmed your email"
                return render_to_response('accounts/confirm.html', args)

            # Если все условия соблюдены, то активируем юзера и выбрасываем сообщение об успешной активации
            user.is_active = True
            user.save()
            args['success'] = "You have confirmed your email"
            return render_to_response('accounts/confirm.html', args)

        # Ловим ошибку, если пользователь или его хеш не найдены.
        except ObjectDoesNotExist:
            args['fail'] = "No hash code like this"
            return render_to_response('accounts/confirm.html', args)

    @staticmethod
    def resend_email(request):
        username = request.GET['username']
        user = User.objects.get(username=username)
        SecretHashCode(user_id=user.pk,
                       hashcode=''.join(
                           random.choice(string.ascii_uppercase + string.digits) for _ in range(12)),
                       expired_date=datetime.now(timezone.utc) + timedelta(minutes=60)
                       ).save()
        email = user.email
        hash_code = user.hashcode
        return send_email(username=username, email=email, hash_code=hash_code)


class PasswordChangeView(View):
    @staticmethod
    def get(request):
        if request.user.is_authenticated:
            args = {}
            args.update(csrf(request))
            return render_to_response("accounts/settings.html", args)
        return render(request, 'accounts/http404.html')

    @staticmethod
    def post(request):
        if request.user.is_authenticated:
            args = {}
            args.update(csrf(request))
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                args['success'] = 'Success'
                return render_to_response('accounts/settings.html', args)
            else:
                args['error'] = form.errors
                return render_to_response("accounts/settings.html", args)
        return redirect('/accounts/settings')
