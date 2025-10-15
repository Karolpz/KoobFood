from django.db import models

class Reservation(models.Model):
    reservation_date = models.DateTimeField()
    number_of_people = models.IntegerField()
    customer_message = models.TextField(blank=True, null=True)
    restaurant = models.ForeignKey('restaurant.Restaurant', on_delete=models.CASCADE)
    customuser = models.ForeignKey('users.CustomUser', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation pour {self.number_of_people} personnes à {self.restaurant.name} le {self.reservation_date.strftime('%Y-%m-%d %H:%M')}"
    
class Reservation_Table(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    restaurant_table = models.ForeignKey('restaurant.Restaurant_Table', on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.reservation.reservation_date.strftime('%Y-%m-%d %H:%M')} : Table n°{self.restaurant_table.table_number} - {self.reservation.number_of_people} personnes"
    
