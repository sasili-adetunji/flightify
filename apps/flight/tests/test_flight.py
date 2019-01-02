# from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.flight.models import Flight
from unittest.mock import patch
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework_jwt import utils
import time

from apps.files.services import MockStore
from apps.files import services as file_services
User = get_user_model()


mockstore = MockStore()

def generate_token(user):
    assert(isinstance(user, User))
    token = utils.jwt_encode_handler(
        utils.jwt_payload_handler(user)
    )

    return '{0} {1}'.format(settings.JWT_AUTH['JWT_AUTH_HEADER_PREFIX'], token)



class FlightTest(APITestCase):

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
        self.data = {
            'username': 'tester',
            'password': 'samplepassowrd'
        }


        self.data = {
            'depart_date': '2222-02-02T20:00:00Z',
            'return_date': '2222-03-02T20:00:00Z',
            'departure': 'London',
            'destination': 'Lagos',
            'fare': Flight.ONE_WAY,
            # 'booked': '',
        }

class FlightTestExceptions(FlightTest):
    """
    Test class for valid flight reservation.
    """

    def test_create_flight_reservation_without_depart_date(self):

        data = self.data.copy()
        data.pop('depart_date')

        response = self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)


    def test_create_flight_reservation_without_departure(self):

        data = self.data.copy()
        data.pop('departure')

        response = self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertContains(response, 'required', status_code=400)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=400)

    def test_create_flight_reservation_with_empty_departure(self):

        data = self.data.copy()
        data['departure'] = ''

        response = self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'blank', status_code=400)
        self.assertContains(response, 'This field may not be blank.', status_code=400)


    def test_list_users_invalid_date(self):
  
        data = self.data.copy()

        self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )


        response = self.client.get(
            reverse(
                'flights-list-users', args = ['1010101']
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertContains(response, 'Provide proper date', status_code=500)


class FlightTestValid(FlightTest):
    """
    Test class for valid flight reservation.
    """

    def test_create_flight_reservation(self):

        data = self.data.copy()

        response = self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get('message'), 'Flight successfully created.')
        self.assertEqual(Flight.objects.filter(pk=response.data.get('payload')['id']).count(), 1)


    def test_list_flight(self):
  
        data = self.data.copy()

        self.client.post(
            reverse(
                'flights-list',
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
        self.assertEqual(len(response.data.get('payload')), 1)
        self.assertEqual(response.data.get('payload')[0]['flight']['passenger_name'], 'Test User')
        self.assertEqual(response.data.get('payload')[0]['flight']['destination'], data['destination'])


    def test_retrieve_flight(self):
  
        data = self.data.copy()

        flight = self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        response = self.client.get(
            reverse(
                'flights-detail', args = [flight.data.get('payload')['id']]
            ),
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'Flight successfully retrieved.')
        self.assertEqual(response.data.get('payload')['flight']['passenger_name'], 'Test User')
        self.assertEqual(response.data.get('payload')['flight']['destination'], data['destination'])
        self.assertEqual(response.data.get('payload')['flight']['fare'], Flight.ONE_WAY)


    def test_update_flight(self):
  
        data = self.data.copy()

        flight = self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )

        data['departure'] = 'Saudi Arabia'

        response = self.client.put(
            reverse(
                'flights-detail', args = [flight.data.get('payload')['id']]
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'flight successfully updated.')
        self.assertEqual(response.data.get('payload')['passenger_name'], 'Test User')
        self.assertEqual(response.data.get('payload')['departure'], 'Saudi Arabia')


    def test_list_users(self):
  
        data = self.data.copy()

        self.client.post(
            reverse(
                'flights-list',
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )

        response = self.client.get(
            reverse(
                'flights-list-users', args = ['2222-02-02']
            ),
            data=data,
            HTTP_AUTHORIZATION=generate_token(
                self.user
            ),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('message'), 'flight successfully retrieved.')
        self.assertEqual(response.data.get('payload')['users'][0]['username'], 'tester')
