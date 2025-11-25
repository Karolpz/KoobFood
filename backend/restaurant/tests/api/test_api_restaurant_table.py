from koobfood.tests.test_api_user_manager import BaseAPITest
from django.urls import reverse
from rest_framework import status
from restaurant.factories import RestaurantFactory, RestaurantTableFactory

class RestaurantTableCreateAPITest(BaseAPITest):
    def setUp(self):
        self.restaurant = RestaurantFactory.create(manager=self.manager_user)
        self.restaurant_table_create_url = reverse('restaurant:api_restaurant_tables-list', args=[self.restaurant.id])
        self.data_table = {
            'table_number': 1,
            'seats': 4,
            'outdoor': True,
            'is_smoking': True,
            'is_available': True,
            'restaurant': self.restaurant.id
        }
    def test_create_restaurant_table_as_manager(self):
        self.test_authenticated_as_manager()
        response = self.client.post(self.restaurant_table_create_url, self.data_table, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_restaurant_table_as_customer(self):
        self.test_authenticated_as_customer()
        response = self.client.post(self.restaurant_table_create_url, self.data_table, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class RestaurantTableListAPITest(BaseAPITest):
    def setUp(self):
        self.restaurant = RestaurantFactory.create(manager=self.manager_user)
        self.restaurant_table_list_url = reverse('restaurant:api_restaurant_tables-list', args=[self.restaurant.id])
        RestaurantTableFactory.create_batch(3, restaurant=self.restaurant)

    def test_list_restaurant_tables_as_manager(self):
        self.test_authenticated_as_manager()
        response = self.client.get(self.restaurant_table_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

    def test_list_restaurant_tables_as_customer(self):
        self.test_authenticated_as_customer()
        response = self.client.get(self.restaurant_table_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)