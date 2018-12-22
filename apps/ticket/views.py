from rest_framework import (
    viewsets,
    status,
    decorators
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

    @decorators.action(methods=['get'], detail=False, url_path='status/(?P<flight_id>[0-9+\-]+)')
    def ticket_status(self, request, **kwargs):
        ticket = ticket_services.ticket_status(
            request.user,
            flight_id=kwargs.get('flight_id'),
        )
        return APIResponse(ticket,
                status=status.HTTP_200_OK,
                message='ticket status successfully retrieved.'
              )