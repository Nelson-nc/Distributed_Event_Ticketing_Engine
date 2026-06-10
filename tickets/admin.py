from django.contrib import admin
from .models import Ticket, Event

admin.site.register(Event)
admin.site.register(Ticket)
