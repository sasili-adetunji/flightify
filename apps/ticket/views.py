from rest_framework import (
    viewsets,
    status
)
from . import serializers as ticket_serializers
from . import (
    services as ticket_services
)
from apps.helpers.response import APIResponse


class TicketViewSet(viewsets.ViewSet):

    def create(self, request):
        ''' views to create a new ticket'''
        
        ticket = ticket_services.create_tickets(request.user)
        return APIResponse(ticket,
                status=status.HTTP_201_CREATED,
                message='ticket successfully created.'
              )
