from django.test import TestCase
from django.urls import reverse
from users.forms import CustomUserCreationForm
from users.factories import CustomUserFactory

class CustomerFormTest(TestCase):

    def test_customer_form_fields(self):
        form = CustomUserCreationForm()
        expected_fields = [
            'last_name', 'first_name', 'username', 
            'email', 'phone_number', 'password1', 'password2'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_password_mismatch(self):
        user_data = CustomUserFactory.build().__dict__

        user_data.update({
            'password1': 'testpassword123',
            'password2': 'differentpassword123'
        })
        form = CustomUserCreationForm(data=user_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_account_duplicate_username(self):

        user1 = CustomUserFactory(username='johndoe')
        user2_data = CustomUserFactory.build(username='johndoe').__dict__
        user2_data.update({
            'password1': 'anotherpassword123',
            'password2': 'anotherpassword123'
        })
        form = CustomUserCreationForm(data=user2_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)


class SignUpTest(TestCase):
    def test_sign_up(self):
        form_data = {
            'last_name': 'Doe',
            'first_name': 'John',
            'username': 'johndoe',
            'email': 'johndoe@gmail.com',
            'phone_number': '1234567890',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        response = self.client.post(reverse("users:signup"), form_data)

        self.assertEqual(response.status_code, 302)
