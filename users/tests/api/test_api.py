from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class SignUpAPITest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('users:api_signup')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'Bt4Bb@example.com',
            'phone_number': '1234567890',
            'last_name': 'Doe',
            'first_name': 'John'
        }
    def test_user_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])
    
    def test_signup_with_existing_username(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

class TokenAPITest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('users:api_signup')
        self.token_url = reverse('users:token_obtain_pair')
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'Bt4Bb@example.com',
            'phone_number': '1234567890',
            'last_name': 'Doe', 
            'first_name': 'John'
        }   
    def test_token_obtainment(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        response = self.client.post(self.token_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_obtainment_with_invalid_credentials(self):
        self.client.post(self.signup_url, self.user_data, format='json')
        response = self.client.post(self.token_url, {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
    