from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['last_name','first_name','username','email', 'phone_number', 'password1', 'password2']
        labels = {
            'last_name': 'Nom',
            'first_name': 'Prénom',
            'username': 'Nom d\'utilisateur',
            'email': 'Adresse e-mail',
            'phone_number': 'Numéro de téléphone',
            'password1': 'Mot de passe',
            'password2': 'Confirmer le mot de passe',
        }

class CustomUserConnectionForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        labels = {
            'username': 'Nom d\'utilisateur',
            'password': 'Mot de passe',
        }