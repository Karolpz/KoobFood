from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserConnectionForm
from django.urls import reverse

    
class SignUp(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/signup_form.html'
    
    def get_success_url(self):
        return self.request.GET.get('next') or reverse('home:home')

class LogIn(LoginView):
    template_name = 'users/login_form.html'
    authentication_form = CustomUserConnectionForm
    
    def get_success_url(self):
        return self.request.GET.get('next') or reverse('home:home')