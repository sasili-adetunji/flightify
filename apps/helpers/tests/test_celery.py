# from rest_framework.reverse import reverse
# from rest_framework.test import APITestCase
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from apps.flight.models import Flight
# from apps.ticket.models import Passenger
# from unittest.mock import patch
# from django.conf import settings
# from rest_framework_jwt import utils
# import time
# from apps.helpers.tasks import (
#   task_send_email_reminder,
#   send_signup_email_task,
#   send_ticket_email_task
# )


# User = get_user_model()

# class CeleryTest(APITestCase):

#     """
#     Base class for testing Login.
#     """

#     @patch('apps.helpers.email_helper.send_mail')
#     def test_celery(self, send_mail):

#         self.user = {
#             # 'username': 'tester2',
#             'email': 'tester1@gmail.com',
#         }

#         response = send_signup_email_task.apply(args=(self.user)).get()
#         # print(response)
#         self.assertEqual(response, 201)
