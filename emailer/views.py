from django.core import mail
from django.shortcuts import render_to_response

from RecordStudio import settings


def send_email(**kwargs):
    args = {}

    # Send welcome mail
    if len(kwargs) == 6:
        email = kwargs['email']
        username = kwargs['username']
        __hash_code = kwargs['hash_code']
        message = "http://127.0.0.1:8000/accounts/confirm?username=%s&hash=%s" % (username, __hash_code)
        args['register'] = "Вы успешно зарегестрировались на сайте. Осталось подтвердить email"

    elif len(kwargs) == 5:
        email = kwargs['email']
        username = kwargs['username']
        password = kwargs['password']
        message = "Добро пожаловать в команду RecordStudio! Ваш логин и пароль для входа в профиль: %s %s " % \
                  (username, password)

    # resend email
    elif len(kwargs) == 3 and 'hash_code' in kwargs.keys():
        username = kwargs['username']
        email = kwargs['email']
        hash_code = kwargs['hash_code']
        message = "http://127.0.0.1:8000/accounts/confirm?username=%s&hash=%s" % (username, hash_code)
        args['resent'] = "Ссылка для потдверждения почты была отправлена на вашу почту"

    # Send forget password mail
    elif kwargs['email'] and kwargs['username'] and kwargs['password']:
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']
        message = "Your data: " + username + " " + password
        args['forget'] = "Ваш новый пароль успешно отправлен на Ваш email"

    try:
        mail.send_mail('Subject here', message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return render_to_response("emailer/successful_page.html", args)
    except Exception:
        args['email_error'] = "Ошибка при отправке письма на email"
        return render_to_response("emailer/successful_page.html", args)
