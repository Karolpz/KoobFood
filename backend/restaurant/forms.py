from django import forms
from.models import Restaurant, Restaurant_Table

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'capacity', 'phone_number', 'contact_email', 'description', 'location']
        labels = {
            'name': 'Nom du restaurant',
            'capacity': 'Capacité',
            'phone_number': 'Numéro de téléphone',
            'contact_email': 'Adresse e-mail',
            'description': 'Description',
            'location': 'Ville',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class RestaurantTableForm(forms.ModelForm):
    class Meta:
        model = Restaurant_Table
        fields = ['table_number', 'seats', 'outdoor', 'is_smoking', 'is_available']
        labels = {
            'table_number': 'Numéro de la table',
            'seats': 'Nombre de sièges',
            'outdoor': 'Extérieur',
            'is_smoking': 'Fumeur',
            'is_available': 'Disponible',
        }
