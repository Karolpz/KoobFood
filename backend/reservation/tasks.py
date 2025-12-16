
from celery import shared_task
from .models import Reservation
from users.models import CustomUser
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Count
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import logging

logger = logging.getLogger('koobfood')

def send_mail_reservation(subject, template_name, context, recipient_list):
    html_content = render_to_string(template_name, context)
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email='no-reply@koobfood.com',
        to=recipient_list
    )
    
    email.attach_alternative(html_content, "text/html")
    
    try:
        email.send()
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'email: {e}")

@shared_task
def send_mail_daily_reservation():
    today = timezone.now().date()
    reservations = Reservation.objects.filter(reservation_date__date=today)
    restaurants = reservations.values("restaurant__name").annotate(total=Count("id"))

    context = {
        'date': today,
        'restaurants': restaurants,
        'reservations': reservations,
    }

    send_mail_reservation(
        subject='Rapport quotidien des réservations KoobFood',
        template_name='email/reservation_report.html',
        context=context,
        recipient_list=['example@gmail.com'],
    )

    return "Email quotidien des réservations envoyé."

@shared_task
def send_mail_after_reservation_manager(reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    manager = reservation.restaurant.manager
    
    context = {
        'reservation': reservation,
    }

    send_mail_reservation(
        subject='Nouvelle réservation sur KoobFood',
        template_name='email/reservation_manager.html',
        context=context,
        recipient_list=[manager.email],
    )

    return "Reservation notification email sent to manager."

@shared_task
def send_mail_after_reservation_customer(reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    customer = reservation.customuser

    context = {
        'reservation': reservation,
    }

    send_mail_reservation(
        subject='Confirmation de votre réservation sur KoobFood',
        template_name='email/reservation_customer.html',
        context=context,
        recipient_list=[customer.email],
    )

    return "Reservation confirmation email sent to customer."
