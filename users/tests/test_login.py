from django.test import TestCase
from django.urls import reverse
from users.factories import CustomUserFactory
from users.forms import CustomUserCreationForm, CustomUserConnectionForm

class LoginFormTest(TestCase):
    def test_login_form(self):
        form = CustomUserConnectionForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)


class LoginConnexionTest(TestCase):
    def setUp(self):
        self.user = CustomUserFactory(username="johndoe", email="johndoe@gmail.com")

    def test_login(self):
        data = {
            'username': 'johndoe',
            'password': 'testpassword123',
        }
        form = CustomUserConnectionForm(data=data)
        self.assertTrue(form.is_valid())

        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, 302)

    def test_login_invalid(self):
        data = {
            'username': 'johndoe',
            'password': 'wrongpassword',
        }
        form = CustomUserConnectionForm(data=data)
        self.assertFalse(form.is_valid())

        response = self.client.post(reverse('users:login'), data)
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='johndoe', password='testpassword123')
        response = self.client.post(reverse('users:logout'))
        self.assertEqual(response.status_code, 302)
