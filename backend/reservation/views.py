from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from .models import Reservation, Reservation_Table
from .forms import ReservationForm
from restaurant.models import Restaurant
from users.models import CustomUser
from restaurant.models import Restaurant_Table
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

import logging

logger = logging.getLogger(__name__)

# -----------------------RESERVATIONS CUSTOMER--------------------------------

def signup_or_login(request, restaurant_id):
    next_url = request.GET.get('next')
    return render(request, 'reservation/signup_or_login.html', {'next': next_url, 'restaurant_id': restaurant_id})

class ReservationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    form_class = ReservationForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["restaurant_id"] = self.kwargs["restaurant_id"]
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse('reservation:reservation_success', kwargs={
            'restaurant_id': self.kwargs['restaurant_id'],
            'reservation_id': self.object.pk
        })
    
    def form_valid(self, form):
        logger.info(f"Nouvelle réservation créée par {self.request.user.username} pour le restaurant ID {self.kwargs['restaurant_id']} le {form.cleaned_data['reservation_date']}.")
        return super().form_valid(form)


class ReservationSuccessView(generic.DetailView):
    model = Reservation
    template_name = 'reservation/reservation_success.html'
    context_object_name = 'reservation'

    def get_object(self):
        return Reservation.objects.get(pk=self.kwargs['reservation_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = Restaurant.objects.get(pk=self.kwargs['restaurant_id'])
        return context


# -----------------------RESERVATIONS MANAGER --------------------------------
class ReservationManagerMixin(LoginRequiredMixin):
    model = Reservation_Table

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(reservation__restaurant__manager=self.request.user)
    
class ReservationManagerListView(ReservationManagerMixin, generic.ListView):
    template_name = 'reservation/reservation_manager_list.html'
    context_object_name = 'reservation_list'

    def get_queryset(self):
      queryset = super().get_queryset()
      return queryset.filter(reservation__restaurant=self.kwargs['restaurant_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()
        context['upcoming_reservations'] = self.get_queryset().filter(reservation__reservation_date__gte=now).order_by('reservation__reservation_date')
        context['past_reservations'] = self.get_queryset().filter(reservation__reservation_date__lt=now).order_by('reservation__reservation_date')
        context['today_reservations'] = self.get_queryset().filter(reservation__reservation_date__date=now.date()).order_by('reservation__reservation_date')
        return context
    
class ReservationManagerDetailView(ReservationManagerMixin, generic.DetailView):
    template_name = 'reservation/reservation_manager_detail.html'
    context_object_name = 'reservation'

