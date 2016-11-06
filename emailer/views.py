from django.core import mail
from django.http import HttpResponse
from RecordStudio import settings

from django.shortcuts import render_to_response


def send_welcome_mail(email, username, password, first_name, last_name, hashs):
    # Требуется отправить сгенерированную ссылку из логина и хеша для подтверждения имейла
    # Send not just a message, but an html message!! (for Jaxy)
    args = {}
    message = "Hello my dear friend! " \
              " You have successfully registered! " \
              " Your login is " + username + "" \
                                             "  Hashcode is " + hashs
    try:
        mail.send_mail('Subject here', message, settings.EMAIL_HOST_USER,
                       [email], fail_silently=False)
        return render_to_response("emailer/successful_page.html", args) # We should redirec the user to the email page
    except Exception:
        args['email_error'] = "Error while sending an email"
        return render_to_response("emailer/successful_page.html", args)


def send_forget_mail(email, username, password):
    args = {}
    message = "Your data: " + username + " " + password
    try:
        mail.send_mail('Subject here', message, settings.EMAIL_HOST_USER,
                       [email], fail_silently=False)
        return render_to_response("emailer/successful_page.html", args) # The same principle
    except Exception:
        args['email_error'] = "Error while sending an email"
        return render_to_response("emailer/successful_page.html", args)
