from koobfood.tests.test_api_user_manager import BaseAPITest
from django.urls import reverse
from rest_framework import status
from reservation.factories import ReservationFactory
from restaurant.factories import RestaurantFactory

class RservationCreateAPITest(BaseAPITest):
    def setUp(self):
        self.restaurant = RestaurantFactory.create()
        self.reservation_create_url = reverse('restaurant:api_reservation-list', args=[self.restaurant.id])
        self.data= {
            'reservation_date': '2025-12-31 19:00',
            'number_of_people': 4,
            'customer_message':'outdoor seating please',
            'customuser': self.customer_user.id,
            'restaurant': self.restaurant.id
        }
    
    def test_create_reservation_as_customer(self):
        self.test_authenticated_as_customer()
        response = self.client.post(self.reservation_create_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reservation_as_unauthenticated(self):
        response = self.client.post(self.reservation_create_url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReservationListAPITest(BaseAPITest):
    def setUp(self):
        self.restaurant = RestaurantFactory.create(manager=self.manager_user)
        self.reservation_list_url = reverse('restaurant:api_reservation-list', args=[self.restaurant.id])
        ReservationFactory.create_batch(1, restaurant=self.restaurant, customuser=self.customer_user)
        ReservationFactory.create_batch(2, restaurant=self.restaurant)

    def test_list_reservations_as_customer(self):
        self.test_authenticated_as_customer()
        response = self.client.get(self.reservation_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

    def test_list_reservations_as_manager(self):
        self.test_authenticated_as_manager()
        response = self.client.get(self.reservation_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

    def test_list_reservations_as_unauthenticated(self):
        response = self.client.get(self.reservation_list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    