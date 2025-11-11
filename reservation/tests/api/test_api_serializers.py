from ...api.serializers import ReservationSerializer
from django.test import TestCase
from restaurant.factories import RestaurantFactory

class ReservationSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'reservation_date': '2025-12-31 19:00',
            'number_of_people': 4,
            'customer_message': 'Looking forward to it!',
        }

    def test_valid_reservation_serializer(self):
        serializer = ReservationSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        reservation_date = serializer.validated_data['reservation_date']
        self.assertEqual(reservation_date.strftime('%Y-%m-%d %H:%M'), '2025-12-31 19:00')
        self.assertEqual(serializer.validated_data['number_of_people'], self.valid_data['number_of_people'])
        self.assertEqual(serializer.validated_data['customer_message'], self.valid_data['customer_message'])

    def test_invalid_reservation_serializer_missing_fields(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['reservation_date']
        serializer = ReservationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('reservation_date', serializer.errors)

    def test_invalid_reservation_serializer_negative_people(self):
        invalid_data = self.valid_data.copy()
        invalid_data['number_of_people'] = -2
        serializer = ReservationSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_readonly_restaurant_field(self):
        restaurant = RestaurantFactory()
        invalid_data = self.valid_data.copy()
        invalid_data['restaurant'] = restaurant.id
        serializer = ReservationSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('restaurant', serializer.validated_data)