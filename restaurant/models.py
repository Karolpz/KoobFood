from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    capacity = models.IntegerField(null=True, blank=True)
    reviews = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='restaurants',
        null=True, blank=True
    )

    def __str__(self):
        return self.name
    
class Restaurant_Table(models.Model):
    table_number = models.IntegerField()
    seats = models.IntegerField()
    outdoor = models.BooleanField(default=False)
    is_smoking = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables')
   
     
    def __str__(self):
        return f"Table {self.table_number} at {self.restaurant.name} ({self.seats} seats) {self.is_available and 'Available' or 'Not Available'}"