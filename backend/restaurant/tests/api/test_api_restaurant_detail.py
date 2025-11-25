from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from restaurant.factories import RestaurantFactory

class RestaurantDetailAPITest(APITestCase):
    def setUp(self):
        self.restaurant = RestaurantFactory.create()
        self.restaurant_detail_url = reverse('restaurant:api_restaurant-detail', args=[self.restaurant.id])

    def test_get_restaurant_detail(self):
        response = self.client.get(self.restaurant_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', response.data)
        self.assertIn('capacity', response.data)
        self.assertIn('reviews', response.data)
        self.assertIn('description', response.data)
        self.assertIn('contact_email', response.data)
        self.assertIn('phone_number', response.data)
        self.assertIn('location', response.data)