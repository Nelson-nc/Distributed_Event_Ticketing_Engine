from django.urls import path
from .views import EventListView, reserve_ticket_view, paystack_webhook_view

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:event_id>/reserve/', reserve_ticket_view, name='reserve-ticket'),
    path('payments/webhook/', paystack_webhook_view, name='paystack-webhook'),
]
