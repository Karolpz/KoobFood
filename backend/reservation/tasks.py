
from celery import shared_task
from .models import Reservation
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Count
@shared_task
def send_mail_daily_reservation():
    today = timezone.now().date()
    reservations = Reservation.objects.filter(reservation_date__date=today)

    if reservations.exists():
        content = (
            f"Le site a enregistré {reservations.count()} réservations pour aujourd'hui.\n"
            "Voici les détails :\n"
        )
        restaurants = reservations.values("restaurant__name").annotate(total=Count("id"))

        for item in restaurants:
            content += f"- Restaurant : {item['restaurant__name']} - Réservations : {item['total']}\n"

    else:
        content = "Aucune réservation pour aujourd'hui."

    send_mail(
        subject='Daily Reservation on KoobFood',
        message=content,
        from_email='no-reply@koobfood.com',
        recipient_list=["carolinelpz34@gmail.com"],
    )

    return "Daily reservation email sent."