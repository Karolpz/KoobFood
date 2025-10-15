import factory
from factory.django import DjangoModelFactory

from restaurant.models import Restaurant, Restaurant_Table
from users.models import CustomUser


class RestaurantFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant

    name = factory.Faker("company")
    capacity = factory.Faker("random_int", min=10, max=100)
    reviews = factory.Faker("pyfloat", left_digits=1, right_digits=1, min_value=1, max_value=5)
    description = factory.Faker("paragraph")
    contact_email = factory.Faker("email")
    phone_number = factory.Faker("numerify", text="###########") 
    location = factory.Faker("address")

    manager = factory.SubFactory("users.factories.CustomUserFactory")


class RestaurantTableFactory(DjangoModelFactory):
    class Meta:
        model = Restaurant_Table

    table_number = factory.Sequence(lambda n: n + 1)
    seats = factory.Faker("random_int", min=2, max=8)
    outdoor = factory.Faker("boolean")
    is_smoking = factory.Faker("boolean")
    is_available = factory.Faker("boolean", chance_of_getting_true=90)

    restaurant = factory.SubFactory(RestaurantFactory)
