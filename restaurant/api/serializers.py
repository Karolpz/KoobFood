from ..models import Restaurant, Restaurant_Table
from rest_framework import serializers

class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant_Table
        fields = '__all__'
        read_only_fields = ['restaurant']

class RestaurantSerializer(serializers.ModelSerializer):
    tables = RestaurantTableSerializer(many=True, read_only=True)
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'capacity',
            'reviews',
            'description',
            'contact_email',
            'phone_number',
            'location',
            'manager',
            'tables'
            ]

