from rest_framework import (
    viewsets,
    status
)
from . import (
    services as flight_services
)
from apps.helpers.response import APIResponse


class FlightViewSet(viewsets.ViewSet):

    def create(self, request):
        ''' views to create a new flight'''
        
        flight = flight_services.create_flight(request.user, data=request.data)
        return APIResponse(flight,
                status=status.HTTP_201_CREATED,
                message='Flight successfully created.'
              )

    def list(self, request):
        ''' views to list flight'''
  
        flight = flight_services.list_flights(
            request.user,
            profile_pk=request.user.pk
        )
        return APIResponse(flight,
                status=status.HTTP_200_OK,
                message='Flight successfully retrieved.'
              )

    def retrieve(self, request, pk):
        ''' views to retrieve a flight'''
  
        flight = flight_services.retrieve_flight(
            request.user,
            flight_pk=pk
        )
        return APIResponse(flight,
                status=status.HTTP_200_OK,
                message='Flight successfully retrieved.'
              )

    def update(self, request, pk):
        ''' views to update a flight'''
  
        flight = flight_services.update_flight(
                request.user,
                flight_pk=pk,
                data=request.data
        )
        return APIResponse(flight,
                status=status.HTTP_200_OK,
                message='flight successfully updated.'
              )