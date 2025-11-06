from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from restaurant.factories import RestaurantFactory
from django.contrib.auth.models import Group, Permission

class RestaurantListAPITest(APITestCase):
    def setUp(self):
        self.restaurant_list_url = reverse('restaurant:api_restaurant-list')
        RestaurantFactory.create_batch(5)

    def test_get_restaurant_list(self):
        response = self.client.get(self.restaurant_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 5)
        for restaurant in response.data:
            self.assertIn('name', restaurant)
            self.assertIn('capacity', restaurant)
            self.assertIn('reviews', restaurant)
            self.assertIn('description', restaurant)
            self.assertIn('contact_email', restaurant)
            self.assertIn('phone_number', restaurant)
            self.assertIn('location', restaurant)

class RestaurantListManagerAPITest(APITestCase):
    def setUp(self):
        self.restaurant_manager_list_url = reverse('restaurant:api_restaurant-my-restaurants')
        restaurant_list = RestaurantFactory.create_batch(3)

    def test_get_restaurant_manager_list_unauthenticated(self):
        response = self.client.get(self.restaurant_manager_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)