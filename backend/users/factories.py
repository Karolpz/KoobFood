import factory
from factory.django import DjangoModelFactory
from django.contrib.auth.hashers import make_password
from faker import Faker

from users.models import CustomUser


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')