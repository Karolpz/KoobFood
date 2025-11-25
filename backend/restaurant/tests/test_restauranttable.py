from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from users.factories import CustomUserFactory
from restaurant.factories import RestaurantFactory


class RestaurantTableCreatePermissionTest(TestCase):
    def setUp(self):
        self.manager_group, _ = Group.objects.get_or_create(name="Manager")
        permission = Permission.objects.get(codename="add_restaurant_table")
        self.manager_group.permissions.add(permission)

        # 🔸 Utilisateurs via factory
        self.user = CustomUserFactory(username="normaluser")
        self.user.set_password("password123")
        self.user.save()

        self.manager = CustomUserFactory(username="manageruser")
        self.manager.set_password("password123")
        self.manager.save()
        self.manager.groups.add(self.manager_group)

        self.restaurant = RestaurantFactory()

    def test_non_manager_cannot_access_create_view(self):
        self.client.login(username="normaluser", password="password123")
        response = self.client.get(reverse("restaurant:restaurant_table_create", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 403)

    def test_manager_can_access_create_view(self):
        self.client.login(username="manageruser", password="password123")
        response = self.client.get(reverse("restaurant:restaurant_table_create", args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
