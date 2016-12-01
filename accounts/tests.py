from django.contrib.auth.models import User, Group
from django.test import Client
from django.test import TestCase

from .forms import UserCreationForm, SoundmanCreationForm


class LoginTest(TestCase):
    def setUp(self):
        user = User.objects.create(username='tester')
        user.set_password("Tester123")
        Group.objects.create(name="Customers").save()
        Group.objects.get(name='Customers').user_set.add(user)
        user.save()

        admin = User.objects.create(username='administrator')
        admin.set_password("Admin123")
        Group.objects.create(name="Administrators").save()
        Group.objects.get(name='Administrators').user_set.add(admin)
        admin.save()

    def test_login_get(self):
        response = self.client.get('/accounts/login')
        self.assertEqual(response.status_code, 200)

    def test_user_login_post(self):
        response = self.client.post('/accounts/login', {'username': 'tester', 'password': 'Tester123'})
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_admin_login_post(self):
        response = self.client.post('/accounts/login', {'username': 'administrator', 'password': 'Admin123'})
        self.assertEqual(response.status_code, 404)


class RegisterTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='tester', email="bekzat.983@mail.ru")
        self.user.set_password("Tester123")
        Group.objects.create(name="Customers").save()
        Group.objects.get(name='Customers').user_set.add(self.user)
        self.user.save()

    def test_if_username__is_exists(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': 'tester', 'password1': '2251452Bb', 'password2': '2251452Bb',
                     'email': 'bekzat@mail.ru'}
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_if_email__is_exists(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': 'smbkzt', 'password1': '2251452Bb', 'password2': '2251452Bb',
                     'email': 'bekzat.983@mail.ru'}
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': 'smbkzt', 'password1': '2251452Bb', 'password2': '2251452Bb',
                     'email': 'bekzat.98@mail.ru'}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': 'smbkzt', 'password1': '1234566789', 'password2': '123456789',
                     'email': 'bekzat.98@mail.ru'}
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_register_get(self):
        response = self.client.get('/accounts/register')
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get('/accounts/register')
        self.assertContains(response, '404.png')


class SoundmanAddTet(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='admin')
        self.admin.set_password("Aadmin123")
        Group.objects.create(name="Administrators").save()
        Group.objects.get(name='Administrators').user_set.add(self.admin)
        self.admin.save()

    # def test_post_request(self):
    #     self.client.force_login(self.admin)
    #     response = self.client.post('/staff/add', {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
    #                                                'username': "smbkzt", "email": "smbekzat@hotmail.com"})
    #     self.assertTrue(response, 200)

    def test_form_is_valid(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': "smbkzt", "email": "smbekzat@hotmail.com"}
        form = SoundmanCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_soundman_exists(self):
        form_data = {'first_name': 'Bekzat', 'last_name': 'Shayakhmetov',
                     'username': "admin", "email": "smbekzat@hotmail.com"}
        form = SoundmanCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


# class StaffPageTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create(username='tester')
#         self.user.set_password("Tester123")
#         Group.objects.create(name="Customers").save()
#         Group.objects.get(name='Customers').user_set.add(self.user)
#         self.user.save()
#
#         self.admin = User.objects.create(username='admin')
#         self.admin.set_password("Tester123")
#         Group.objects.create(name="Administrators").save()
#         Group.objects.get(name='Administrators').user_set.add(self.admin)
#         self.admin.save()

    # def test_user_get(self):
    #     self.client.get('/staff/')
    #     response = self.client.post('/staff/', {'login': 'admin', 'password': 'Tester123'})
    #     self.assertTemplateUsed(response, 'administrators_page.html')

    # def test_staff_login_post(self):
    #     self.client.force_login(user=self.admin)
    #     response = self.client.get('/staff/profile')
    #     self.assertContains(response, "Брони")


class BookingPageTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_booking_post(self):
        response = self.client.post('/accounts/login', {'username': 'tester', 'password': 'Jaxonyo23'})
        self.assertEquals(response.status_code, 200)

    def test_booking_get(self):
        self.client.post('/accounts/login', {'username': 'tester', 'password': 'Jaxonyo23'})
        response = self.client.get('/step_1/')
        self.assertEquals(response.status_code, 302)
