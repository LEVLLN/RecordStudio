from django.core import mail

from RecordStudio import settings


def send_welcome_mail(email, username, password, first_name, last_name):
    message = "Hello my dear friend! " \
              " You have successfully registered! " \
              " Your login is " + username + "" \
                                             "  Password is " + password + " First Name " + first_name + " " \
                                                                                                         "Last Name" + last_name

    mail.send_mail('Subject here', message, settings.EMAIL_HOST_USER,
                   [email], fail_silently=False)


def send_forget_mail(email, username, password):
    message = "Your data: " + username + " " + password

    mail.send_mail('Subject here', message, settings.EMAIL_HOST_USER,
                   [email], fail_silently=False)