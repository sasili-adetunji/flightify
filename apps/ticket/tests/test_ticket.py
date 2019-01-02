from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.flight.models import Flight
from apps.ticket.models import Passenger
from unittest.mock import patch
from django.conf import settings
from rest_framework_jwt import utils
import time

User = get_user_model()


def generate_token(user):
    assert(isinstance(user, User))
    token = utils.jwt_encode_handler(
        utils.jwt_payload_handler(user)
    )

    return '{0} {1}'.format(settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'], token)



class TicketTest(APITestCase):

    """
    Base class for testing Login.
    """

    def setUp(self):

        self.user = User.objects.create_user(
            email='testuser@example.com', password='samplepassowrd',
            username='tester',
            first_name='Test',
            last_name='User'
        )

        # self.flight = Flight.objects.create(
        #     passenger = self.user,
        #     depart_date = '2222-02-02T20:00:00Z',
        #     return_date =  '2222-03-02T20:00:00Z',
        #     departure = 'LOS',
        #     destination =  'Lagos',
        #     fare =  Flight.ONE_WAY,
        # )


        # self.passenger = Passenger.objects.create(
        #     flight = self.flight,
        #     birth_date = '2222-03-02',
        #     phone = '0809999999',
        #     passport_number = 'A1231',
        #     contact_address =  'some address',
        #     contact_kin_name =  'someone',
        #     contact_kin_relationship = 'brother',
        #     contact_kin_phone =  '123456789',
        #     contact_kin_email =  'sas@email.com',
        # )
        self.flight_data = {
                'depart_date': '2222-02-02T20:00:00Z',
                'return_date': '2222-03-02T20:00:00Z',
                'departure': 'London',
                'destination': 'Lagos',
                'fare': Flight.ONE_WAY,
            }

        self.data = {
            'flight': 1,
            'birth_date': '2222-03-02',
            'phone': '0809999999',
            'passport_number': 'A1231',
            'contact_address': 'some address',
            'contact_kin_name': 'someone',
            'contact_kin_relationship': 'brother',
            'contact_kin_phone': '123456789',
            'contact_kin_email': 'sas@email.com',
        }


class TicketTestValid(TicketTest):
    """
    Test class for valid ticket reservation.
    """

    def test_create_flight_reservation(self):


        flight_data = self.flight_data.copy()

        flight_response = self.client.post(
              reverse(
                  'flights-list',
              ),
              data=flight_data,
              HTTP_AUTHORIZATION=generate_token(
                  self.user
              ),
          )
        data = self.data.copy()
        data['flight'] = flight_response.data.get('payload')['id']
        response = self.client.post(
            reverse(
                'tickets-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('message'), 'ticket successfully booked.')
        self.assertEqual(response.data.get('payload')['ticket_detail']['user_email'], 'testuser@example.com')


    def test_list_ticket_status(self):
  
        data = self.data.copy()
        
        flight_data = self.flight_data.copy()

        flight_response = self.client.post(
              reverse(
                  'flights-list',
              ),
              data=flight_data,
              HTTP_AUTHORIZATION=generate_token(
                  self.user
              ),
        )


        self.client.get(
            reverse(
                'tickets-ticket-status', args= [flight_response.data.get('payload')['id']]
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        response = self.client.get(
            reverse(
                'flights-list',
            ),
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Flight successfully retrieved.')
        self.assertEqual(response.data.get('payload')[0]['flight']['passenger_name'], 'Test User')
        self.assertEqual(response.data.get('payload')[0]['flight']['destination'], 'Lagos')
