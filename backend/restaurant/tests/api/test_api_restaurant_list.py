from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from restaurant.factories import RestaurantFactory
from django.contrib.auth.models import Group, Permission
from koobfood.tests.test_api_user_manager import BaseAPITest

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

class RestaurantListManagerAPITest(BaseAPITest):
    def setUp(self):
        self.restaurant_manager_list_url = reverse('restaurant:api_restaurant-my-restaurants')
        RestaurantFactory.create_batch(1, name ='resto random')
        RestaurantFactory.create_batch(1, name ='resto manager', manager = self.manager_user)

    def test_get_restaurant_manager_list_as_manager(self):
        self.test_authenticated_as_manager()
        response = self.client.get(self.restaurant_manager_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resto manager', [restaurant['name'] for restaurant in response.data])
        self.assertNotIn('resto random', [restaurant['name'] for restaurant in response.data])

    def test_get_restaurant_manager_list_as_user(self):
        self.test_authenticated_as_customer()
        response = self.client.get(self.restaurant_manager_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

