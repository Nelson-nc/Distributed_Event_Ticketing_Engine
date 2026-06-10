from celery import shared_task
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from .models import Ticket, Event
import logging

logger = logging.getLogger(__name__)

@shared_task
def clean_expired_reservations():
    expiration_time = timezone.now() - timedelta(minutes=5)
    expired_tickets = Ticket.objects.filter(status='RESERVED', reserved_at__lte=expiration_time)

    expired_count = expired_tickets.count()
    if expired_count == 0:
        return "No expired reservation found."

    for ticket in expired_tickets:
        with transaction.atomic():
            event = ticket.event
            event.tickets_available += 1
            event.save()

            logger.info(f"Ticket {ticket.id} expired. Returned 1 spot to Event: {event.title}")
            ticket.delete()

    return f"Successfully cleaned up {expired_count} expired ticket reservations."
