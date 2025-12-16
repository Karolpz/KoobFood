from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserConnectionForm
from django.urls import reverse

import logging

logger = logging.getLogger(__name__)

    
class SignUp(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'users/signup_form.html'
    
    def get_success_url(self):
        return self.request.GET.get('next') or reverse('home:home')
    
    def form_valid(self, form):
        logger.info(f"Nouveau utilisateur inscrit, bienvenue {self.request.user.username}!")
        return super().form_valid(form)

class LogIn(LoginView):
    template_name = 'users/login_form.html'
    authentication_form = CustomUserConnectionForm
    
    def get_success_url(self):
        return self.request.GET.get('next') or reverse('home:home')
    
    def form_valid(self, form):
        logger.info(f"Utilisateur connecté: {form.get_user().username}")
        return super().form_valid(form)
    
class LoggerLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        logger.info(f"Utilisateur déconnecté: {request.user.username}")
        return super().dispatch(request, *args, **kwargs)

