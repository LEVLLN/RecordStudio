import unittest

from django.test import Client

from .forms import UserCreationForm, SoundmanCreationForm


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_get(self):
        response = self.client.get('/accounts/login')
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        response = self.client.post('/accounts/login', {'username': 'tester', 'password': 'Jaxonyo23'})
        self.assertEquals(response.status_code, 200)


class RegisterTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_form(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': 'smbkzt', 'password1': '2251452Bb', 'password2': '2251452Bb',
                     'email': 'bekzat.98@mail.ru'}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_register_get(self):
        response = self.client.get('/accounts/register')
        self.assertEqual(response.status_code, 200)


class SoundmanAddTet(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_form(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': "smbkzt", "email": "smbekzat@hotmail.com"}
        form = SoundmanCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class StaffPageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get('/staff/')
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        response = self.client.post('/staff/', {'login': 'admin', 'password': 'qwertY123'})
        self.assertEquals(response.status_code, 200)


class BookingPageTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_booking_post(self):
        response = self.client.post('/accounts/login', {'username': 'tester', 'password': 'Jaxonyo23'})
        self.assertEquals(response.status_code, 200)

    def test_booking_get(self):
        self.client.post('/accounts/login', {'username': 'tester', 'password': 'Jaxonyo23'})
        response = self.client.get('/step_1/')
        self.assertEquals(response.status_code, 302)
