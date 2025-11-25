from ...api.serializers import CustomUserSerializer
from django.test import TestCase

class CustomUserSerializerTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'Bt4Bb@example.com',   
            'phone_number': '1234567890'
        }
    def test_valid_signup_serializer(self):
        serializer = CustomUserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())  
        self.assertEqual(serializer.validated_data['username'], self.valid_data['username'])
        self.assertEqual(serializer.validated_data['email'], self.valid_data['email'])
        self.assertEqual(serializer.validated_data['phone_number'], self.valid_data['phone_number'])
        self.assertEqual(serializer.validated_data['password'], self.valid_data['password'])

    def test_invalid_signup_serializer_missing_fields(self):
        invalid_data = self.valid_data.copy()
        del invalid_data['username']
        serializer = CustomUserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_password_write_only(self):
        serializer = CustomUserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        serialized_data = serializer.data
        self.assertNotIn('password', serialized_data)