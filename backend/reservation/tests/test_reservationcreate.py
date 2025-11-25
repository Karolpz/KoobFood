from django.test import TestCase
from django.urls import reverse
from restaurant.models import Restaurant, Restaurant_Table
from reservation.models import Reservation, Reservation_Table
from users.models import CustomUser
from reservation.forms import ReservationForm

class CreateReservationTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.restaurant = Restaurant.objects.create(
            name='Testaurant',
            location='123 Test St',
            phone_number='1234567890'
        )
        self.table1 = Restaurant_Table.objects.create(
            restaurant=self.restaurant,
            table_number=1,
            seats=4
        )

    def test_create_reservation(self):
        self.client.login(username='testuser', password='testpassword123')
        data = {
            'restaurant_id': self.restaurant.id,
            'reservation_date': '2025-12-31 19:00',
            'number_of_people': 4,
        }
        form = ReservationForm(data=data)
        self.assertTrue(form.is_valid())

        response = self.client.post(
        reverse('reservation:reservation_create', args=[self.restaurant.id]),
         data
        )

        self.assertEqual(response.status_code, 302)
        reservation = Reservation.objects.get(customuser=self.user, restaurant=self.restaurant)
        self.assertTrue(Reservation_Table.objects.filter(reservation=reservation, restaurant_table=self.table1).exists())

    def test_reservation_form_invalid(self):
        data = {
            "reservation_date": "2025-12-31 19:00",
            "number_of_people": 10,
        }
        form = ReservationForm(
            data=data,
            user=self.user,
            restaurant_id=self.restaurant.id
        )
        self.assertFalse(form.is_valid())
        self.assertIn("number_of_people", form.errors)
        self.assertEqual(form.errors["number_of_people"], ["Aucune table disponible pour ce nombre de personnes."])

    def test_reservation_form_past_date(self):
        data = {
            "reservation_date": "2020-01-01 19:00",
            "number_of_people": 2,
        }
        form = ReservationForm(
            data=data,
            user=self.user,
            restaurant_id=self.restaurant.id
        )
        self.assertFalse(form.is_valid())
        self.assertIn("reservation_date", form.errors)
        self.assertEqual(form.errors["reservation_date"], ["La date doit être dans le futur."])

    def test_reservation_form_number_of_people(self):
        data = {
            "reservation_date": "2025-12-31 19:00",
            "number_of_people": 0,
        }
        form = ReservationForm(
            data=data,
            user=self.user,
            restaurant_id=self.restaurant.id
        )
        self.assertFalse(form.is_valid())
        self.assertIn("number_of_people", form.errors)
        self.assertEqual(form.errors["number_of_people"], ["Le nombre de personnes doit être supérieur à zéro."])

    
