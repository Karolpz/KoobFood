from django.urls import reverse
from rest_framework.test import APITestCase
from users.factories import CustomUserFactory
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from users.models import CustomUser
from django.contrib.auth.models import Group, Permission

class UserManagerAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager_group, _ = Group.objects.get_or_create(name="Manager")

        cls.customer_user = CustomUserFactory(username="customeruser")
        cls.customer_user.set_password("password123")
        cls.customer_user.save()

        cls.manager_user = CustomUserFactory(username="manageruser")
        cls.manager_user.set_password("password123")
        cls.manager_user.save()
        cls.manager_user.groups.add(cls.manager_group)

        cls.customer_user_token = str(AccessToken.for_user(cls.customer_user))
        cls.manager_user_token = str(AccessToken.for_user(cls.manager_user))

    def test_authenticated_as_customer(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.customer_user_token)

    def test_authenticated_as_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.manager_user_token)