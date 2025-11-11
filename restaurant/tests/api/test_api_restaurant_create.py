from koobfood.tests.test_api_user_manager import BaseAPITest
from django.urls import reverse
from rest_framework import status

class RestaurantCreateManagerAPITest(BaseAPITest):
    def setUp(self):
        self.restaurant_create_url = reverse('restaurant:api_restaurant-list')
        self.data= {
            'name': 'Manager Resto',
            'capacity': 100,
            'description': 'A new restaurant',
            'contact_email': 'managerresto@gmail.com',
            'phone_number': '1234567890',
            'location': 'New York'
        }
    def test_create_restaurant_as_manager(self):
        self.test_authenticated_as_manager()
        response = self.client.post(self.restaurant_create_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_restaurant_as_customer(self):
        self.test_authenticated_as_customer()
        response = self.client.post(self.restaurant_create_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)