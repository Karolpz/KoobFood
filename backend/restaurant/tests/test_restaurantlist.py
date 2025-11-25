from django.test import TestCase
from django.urls import reverse
from restaurant.models import Restaurant
from restaurant.factories import RestaurantFactory

class RestaurantListViewTest(TestCase):
    def setUp(self):
        self.restaurant1 = RestaurantFactory(name="Test 1")
        self.restaurant2 = RestaurantFactory(name="Test 2")

    def test_queryset_restaurants(self):
        restaurants = Restaurant.objects.all()
        self.assertEqual(restaurants.count(), 2)
        self.assertEqual(restaurants[0].name, "Test 1")
        self.assertEqual(restaurants[1].name, "Test 2")


class RestaurantListViewIntegrationTest(TestCase):
    def setUp(self):
        self.restaurant1 = RestaurantFactory(name="Test 1")
        self.restaurant2 = RestaurantFactory(name="Test 2")

    def test_restaurant_list_view(self):
        response = self.client.get(reverse('restaurant:restaurants_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test 1")
        self.assertContains(response, "Test 2")
        self.assertTemplateUsed(response, 'restaurant/restaurant_list.html')
