from django.test import TestCase
from django.urls import reverse
from restaurant.models import Restaurant, Restaurant_Table
from reservation.models import Reservation, Reservation_Table
from users.models import CustomUser
from reservation.forms import ReservationForm
from django.contrib.auth.models import Group, Permission

class ReservationListViewTest(TestCase):
    def setUp(self):
        self.manager_group, _ = Group.objects.get_or_create(name="Manager")

        self.manager = CustomUser.objects.create_user(
            username="manageruser",
            password="password123"
        )
        self.manager.groups.add(self.manager_group)

        self.user = CustomUser.objects.create_user(
            username="normaluser",
            password="password123"
        )

        self.restaurant = Restaurant.objects.create(
            name="Testaurant",
            location="123 Test St",
            phone_number="1234567890"
        )

        self.table1 = Restaurant_Table.objects.create(
            restaurant=self.restaurant,
            table_number=1,
            seats=4
        )

    def test_reservation_list_view(self):
        self.client.login(username='manageruser', password='password123')
        response = self.client.get(reverse('reservation:reservation_manager_list', args=[self.restaurant.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation/reservation_manager_list.html')