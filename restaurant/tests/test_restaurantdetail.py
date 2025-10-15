from django.test import TestCase
from django.urls import reverse
from restaurant.models import Restaurant
from users.models import CustomUser
from django.contrib.auth.models import Group, Permission

class RestaurantDetailViewTest(TestCase):
    def setUp(self):
        self.restaurant = Restaurant.objects.create(name="Test Detail", location="789 Test Blvd", phone_number="1122334455")

    def test_restaurant_detail_view(self):
        response = self.client.get(reverse('restaurant:restaurant_detail', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Detail")
        self.assertTemplateUsed(response, 'restaurant/restaurant_detail.html')