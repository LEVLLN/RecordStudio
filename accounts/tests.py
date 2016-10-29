from django.test import TestCase, Client
from django.contrib.auth import authenticate

from .forms import UserCreationForm
import unittest


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def login_get(self):
        response = self.client.get('/accounts/login')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'login.html')

    def login_post(self):
        response = self.client.post('/accounts/login', {'username':'admin', 'password':'qwertY123'})
        self.assertEquals(response.status_code, 200)


class RegisterTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_form(self):
        form_data = {'first_name':'Bekzat', 'last_name':'Shayakhmetov',
                                    'username':'smbkzt', 'password1':'2251452Bb', 'password2':'2251452Bb', 'email':'bekzat.98@mail.ru'}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_get(self):
        response = self.client.get('/accounts/register')
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        data = {'first_name':'Bekzat', 'last_name':'Shayakhmetov','username':'smbkzt', 'password1':'2251452Bb', 'password2':'2251452Bb', 'email':'bekzat.98@mail.ru'}
        response = self.client.post('/accounts/register', data)
        self.client.login(username='smbkzt', password='2251452Bb')
        self.assertEqual(response.status_code, 200)


# class EmailTest(TestCase):
#     def test_send_email(self):
#         mail.send_mail(
#             'Subject here', 'Here is the message.',
#             'from@example.com', ['to@example.com'],
#             fail_silently=False,
#         )
#
#         self.assertEqual(len(mail.outbox), 1)
#
#         self.assertEqual(mail.outbox[0].subject, 'Subject here')
#         mail.outbox = []
