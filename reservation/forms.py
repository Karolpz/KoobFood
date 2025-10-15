from django import forms
from django.utils import timezone
from .models import Reservation, Reservation_Table
from restaurant.models import Restaurant_Table


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["reservation_date", "number_of_people"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.restaurant_id = kwargs.pop("restaurant_id", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        number = cleaned_data.get("number_of_people")
        if number and number <= 0:
            self.add_error("number_of_people", "Le nombre de personnes doit être supérieur à zéro.")

        return cleaned_data

    def clean_reservation_date(self):
        date = self.cleaned_data.get("reservation_date")
        if date and date <= timezone.now():
            raise forms.ValidationError("La date doit être dans le futur.")
        return date

    def clean_number_of_people(self):
        number = self.cleaned_data.get("number_of_people")
        if number and self.restaurant_id:
            table = Restaurant_Table.objects.filter(
                restaurant_id=self.restaurant_id,
                seats__gte=number,
                is_available=True
            ).order_by("seats").first()

            if not table:
                raise forms.ValidationError("Aucune table disponible pour ce nombre de personnes.")
        if number <= 0:
            raise forms.ValidationError("Le nombre de personnes doit être supérieur à zéro.")
        return number

    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.restaurant_id = self.restaurant_id
        reservation.customuser = self.user

        if commit:
            reservation.save()

            table = Restaurant_Table.objects.filter(
                restaurant_id=self.restaurant_id,
                seats__gte=self.cleaned_data["number_of_people"],
                is_available=True
            ).order_by("seats").first()

            if table:
                Reservation_Table.objects.create(reservation=reservation, restaurant_table=table)
                table.is_available = False
                table.save()

        return reservation
