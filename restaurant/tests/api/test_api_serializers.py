from ...api.serializers import RestaurantSerializer, RestaurantTableSerializer
from django.test import TestCase
from ...factories import RestaurantFactory
from users.factories import CustomUserFactory


class RestaurantSerializerTest(TestCase):
    def setUp(self):
        manager_user = CustomUserFactory()
        self.valid_data = {
            'name': 'The Great Eatery',
            'capacity': 100,
            'reviews': 3.5,
            'description': 'A cozy place to enjoy delicious meals.',
            'contact_email': 'K8C4o@example.com',
            'phone_number': '1234567890',
            'location': 'New York',
            'manager': manager_user.id,
        }       

    def test_valid_restaurant_serializer(self):
        serializer = RestaurantSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid()) 
        self.assertEqual(serializer.validated_data['name'], self.valid_data['name'])
        self.assertEqual(serializer.validated_data['capacity'], self.valid_data['capacity'])
        self.assertEqual(serializer.validated_data['reviews'], self.valid_data['reviews'])
        self.assertEqual(serializer.validated_data['description'], self.valid_data['description'])
        self.assertEqual(serializer.validated_data['contact_email'], self.valid_data['contact_email'])
        self.assertEqual(serializer.validated_data['phone_number'], self.valid_data['phone_number'])
        self.assertEqual(serializer.validated_data['location'], self.valid_data['location'])
        self.assertEqual(serializer.validated_data['manager'].id, self.valid_data['manager'])

    def test_invalid_restaurant_serializer_missing_fields(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['name']
        serializer = RestaurantSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

class RestaurantTableSerializerTest(TestCase):
    def setUp(self):
        restaurant = RestaurantFactory()
        self.valid_data = {
            'table_number': 1,
            'seats': 4,
            'outdoor': False,
            'is_smoking': False,
            'is_available': True,
            'restaurant': restaurant.id
        }

    def test_valid_restaurant_table_serializer(self):
        serializer = RestaurantTableSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['table_number'], self.valid_data['table_number'])
        self.assertEqual(serializer.validated_data['seats'], self.valid_data['seats'])
        self.assertEqual(serializer.validated_data['is_available'], self.valid_data['is_available'])
        self.assertEqual(serializer.validated_data['outdoor'], self.valid_data['outdoor'])
        self.assertEqual(serializer.validated_data['is_smoking'], self.valid_data['is_smoking'])

    def test_invalid_restaurant_table_serializer_invalid_fields(self):
        invalid_data = self.valid_data.copy()
        invalid_data['table_number'] = 'Un'
        serializer = RestaurantTableSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('table_number', serializer.errors)

    def test_read_only_restaurant_field(self):
        invalid_data = self.valid_data.copy()
        invalid_data['restaurant'] = 1
        serializer = RestaurantTableSerializer(data=invalid_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertNotIn('restaurant', serialized_data)