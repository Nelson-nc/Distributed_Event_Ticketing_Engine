import hmac
import hashlib
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer


class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_calss = EventSerializer


@api_view(['POST'])
def reserve_ticket_view(request, event_id):
    user = request.user

    if not user.is_authenticated:
        return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        with transaction.atomic():
            event = Event.objects.select_for_update().get(id=event_id)

            if event.tickets_available <= 0:
                return Response({"error": "Tickets are sold out!"}, status=status.HTTP_400_BAD_REQUEST)

            if Ticket.objects.filter(event=event, user=user, status="RESERVED").exists():
                return Response({"error": "You already have a pending reservation for this event"}, status=status.HTTP_400_BAD_REQUEST)

            event.tickets_available -= 1
            event.save()

            ticket = Ticket.objects.create(event=event, user=user, status="RESERVED")
            serializer = TicketSerializer(ticket)

            return Response({
                "message": "Ticket reserved succeessfully! You have 5 minutes to pay.",
                "ticket": serializer.data
            }, status=status.HTTP_201_CREATED)

    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": "An error occured during reservation"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
def paystack_webhook_view(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    paystack_signature = request.headers.get('X-Paystack-Signature')
    if not paystack_signature:
        return HttpResponse(status=401)

    computed_signature = hmac.new(bytes(settings.PAYSTACK_WEBHOOK_SECRET, 'utf-8'), msg=request.body, digestmod=hashlib.sha256).hexdigest()

    if not hmac.compare_digest(computed_signature, paystack_signature):
        return HttpResponse(status=401)

    try:
        payload = json.loads(request.body)
    except ValueError:
        return HttpResponse(status=400)

    event_type = payload.get('event')

    if event_type == 'charge.success':
        data = payload.get('data', {})
        metadata = data.get('metadata', {})
        ticket_id = metadata.get('ticket_id')

        if ticket_id:
            try:
                with transaction.atomic():
                    ticket = Ticket.objects.select_for_update().get(id=ticket_id, status='RESERVED')
                    ticket.status = 'CONFIRMED'
                    ticket.save()
            except Ticket.DoesNotExist:
                print(f"webhook recieved for non-existent or processed ticket: {ticket_id}")
    
    return HttpResponse(status=200)
