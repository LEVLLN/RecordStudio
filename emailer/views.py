from django.core import mail
from django.http import HttpResponse
from django.test import TestCase
from RecordStudio import settings


class EmailTest(TestCase):
    def send(request, email):
        try:
            mail.send_mail('Subject here', 'Here is the message.', settings.EMAIL_HOST_USER,
                  [email], fail_silently=False)
            return HttpResponse("The mail has been sent successfully")
        except Exception:
            return HttpResponse(Exception)
