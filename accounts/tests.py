from django.test import TestCase, Client
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

    def test_register_get(self):
        response = self.client.get('/accounts/register')
        self.assertEqual(response.status_code, 200)

    def test_register_post(self):
        response = self.client.post('/accounts/register', {'first_name':'Bekzat', 'last_name':'Shayakhmetov',
                                                        'username':'smbkzt', 'password1':'2251452Bb', 'password2':"2251452Bb"})
        self.assertEqual(response.status_code, 200)
