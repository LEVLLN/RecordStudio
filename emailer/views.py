from django.core import mail
from django.http import HttpResponse
from RecordStudio import settings


def send(request, username, password, email):
    try:
        message = "Hello my dear friend!" \
                  "You have successfully registered! " \
                  "Your login is " + username + "" \
                  "Password is " + password

        mail.send_mail('Subject here', message, settings.EMAIL_HOST_USER,
                           [email], fail_silently=False)
        return HttpResponse("The mail has been sent successfully")
    except Exception:
        return HttpResponse(Exception)
