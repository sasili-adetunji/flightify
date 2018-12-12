from rest_framework import serializers
from apps.flight.models import Flight


class FlightSerializer(serializers.ModelSerializer):
    """ Flight serializer """

    fare_name = serializers.SerializerMethodField(read_only=True)
    passenger_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'

    def get_fare_name(self, flight):
        fare_dict = dict(Flight.FARE_CHOICES)
        return fare_dict[flight.fare]

    def get_passenger_name(self, flight):
        return flight.passenger.get_full_name()