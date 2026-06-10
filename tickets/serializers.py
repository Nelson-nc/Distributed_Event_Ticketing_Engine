from rest_framework import serializers
from .models import Event, Ticket

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'total_tickets', 'tickets_available']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'user', 'status', 'reserved_at']
