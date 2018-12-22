from rest_framework import (
    viewsets,
    status
)
from . import (
    services as ticket_services
)
from apps.flight.serializers import FlightSerializer
from apps.ticket.serializers import BookTicketSerializer

from apps.helpers.response import APIResponse


class TicketViewSet(viewsets.ViewSet):

    def create(self, request):
        ''' views to create a new ticket'''
        
        ticket = ticket_services.book_tickets(request.user, data=request.data)
        return APIResponse(ticket,
                status=status.HTTP_201_CREATED,
                message='ticket successfully booked.'
              )
