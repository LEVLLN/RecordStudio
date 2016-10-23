from django.core import mail
from django.http import HttpResponse
from RecordStudio import settings


def send(request, email):
    try:
        mail.send_mail('Subject here', 'Here is the message.', settings.EMAIL_HOST_USER,
                       [email], fail_silently=False)
        return HttpResponse("The mail has been sent successfully")
    except Exception:
        return HttpResponse(Exception)
