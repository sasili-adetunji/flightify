from django.db import (
    transaction
)
from rest_framework import exceptions
from . import serializers as flight_serializer

from . import serializers as ticket_serializer
from apps.ticket.models import Passenger
from apps.flight.models import Flight


def book_tickets(requestor, data):
    '''Book a new ticket'''

    ticket_info = data.copy()
    flight = Flight.objects.get(passenger=ticket_info.get('flight'))
    
    result = {}

    serializer = ticket_serializer.BookTicketSerializer(
        data=ticket_info
    )
    with transaction.atomic():
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            result['ticket_detail'] = serializer.data
        flight.booked= True
        flight.save()
        result['flight_detail'] = flight_serializer.FlightSerializer(flight).data

    return result
