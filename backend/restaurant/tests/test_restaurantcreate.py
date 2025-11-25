from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission

from restaurant.forms import RestaurantForm
from users.factories import CustomUserFactory
from restaurant.factories import RestaurantFactory


class RestaurantCreateFormTest(TestCase):
    def test_restaurant_create_form_fields(self):
        form = RestaurantForm()
        expected_fields = [
            'name', 'capacity', 'phone_number',
            'contact_email', 'description', 'location'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)

    def test_valid_restaurant_form(self):
        form_data = {
            'name': 'Test Restaurant',
            'capacity': 100,
            'phone_number': '1234567890',
            'contact_email': 'test@example.com',
            'description': 'This is a test restaurant.',
            'location': 'Test City',
        }
        form = RestaurantForm(data=form_data)
        self.assertTrue(form.is_valid())


class RestaurantCreatePermissionTest(TestCase):
    def setUp(self):
        # 🔹 Création du groupe Manager et ajout du droit add_restaurant
        self.manager_group, _ = Group.objects.get_or_create(name="Manager")
        permission = Permission.objects.get(codename="add_restaurant")
        self.manager_group.permissions.add(permission)

        # 🔹 Utilisateurs créés via factory
        self.normal_user = CustomUserFactory(username="normaluser")
        self.normal_user.set_password("password123")
        self.normal_user.save()

        self.manager_user = CustomUserFactory(username="manageruser")
        self.manager_user.set_password("password123")
        self.manager_user.save()
        self.manager_user.groups.add(self.manager_group)

    def test_non_manager_cannot_access_create_view(self):
        self.client.login(username="normaluser", password="password123")
        response = self.client.get(reverse("restaurant:restaurant_create"))
        self.assertEqual(response.status_code, 403)

    def test_manager_can_access_create_view(self):
        self.client.login(username="manageruser", password="password123")
        response = self.client.get(reverse("restaurant:restaurant_create"))
        self.assertEqual(response.status_code, 200)
