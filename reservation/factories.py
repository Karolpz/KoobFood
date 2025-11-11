import factory
from factory.django import DjangoModelFactory
from django.utils import timezone

from .models import Reservation
from users.factories import CustomUserFactory
from restaurant.factories import RestaurantFactory

class ReservationFactory(DjangoModelFactory):
    class Meta:
        model = Reservation
    
    reservation_date = factory.LazyFunction(lambda: timezone.now())
    number_of_people = factory.Faker("random_int", min=1, max=20)
    customer_message = factory.Faker("sentence", nb_words=6)
    restaurant = factory.SubFactory(RestaurantFactory) 
    customuser = factory.SubFactory(CustomUserFactory)