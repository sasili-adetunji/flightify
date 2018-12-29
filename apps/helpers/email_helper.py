import pytz
from datetime import datetime
from django.db import (
    transaction
)
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from apps.helpers.token import generate_confirmation_token
from apps.flight.models import Flight
from apps.ticket.models import Passenger
from django.conf import settings

def send_signup_confirmation(user):
    """ Email helper to send confirmation email to the user """

    link=generate_confirmation_token(user['email'])
    msg_plain = render_to_string('account/confirm_signup.txt', {'user': user, 'link': link, 'site': settings.DOMAIN_NAME})
    msg_html = render_to_string('account/confirm_signup.html', {'user': user, 'link': link, 'site': settings.DOMAIN_NAME})

    send_mail(
        'Email confirmation on Flightify',
        msg_plain,
        settings.EMAIL_HOST_USER,
        [user['email']],
        html_message=msg_html,
    )


def send_ticket_email(result):

    """ Email helper to send ticket email to the user when a ticket is booked"""

    email = result['ticket_detail']['user_email']
    username = result['ticket_detail']['username']

    msg_plain = render_to_string('ticket/ticket_email.txt', {'result': result, 'username': username})
    msg_html = render_to_string('ticket/ticket_email.html', {'result': result, 'username': username})
    send_mail(
        'Ticket Email on Flightify',
        msg_plain,
        settings.EMAIL_HOST_USER,
        [email],
        html_message=msg_html,
    )


def send_ticket_reminder():

    """ 
    Email helper to send reminder email to the user 
    when departure date is less than 24hrs
    """

    passengers = Passenger.objects.filter(
        flight__reminder_notification_sent_at__isnull=True,
        flight__booked=True
        )

    for passenger in passengers:
        if passenger.flight.reminder_notification_sent_at is None and (passenger.flight.depart_date - datetime.now().replace(tzinfo=pytz.UTC)).total_seconds() <= 24*3600:
            
            email = passenger.flight.passenger.email
            username = passenger.flight.passenger.username

            departure = passenger.flight.departure

            msg_plain = render_to_string('reminder/reminder_email.txt', { 'username': username, 'departure': departure})
            msg_html = render_to_string('reminder/reminder_email.html', { 'username': username, 'departure': departure})

            send_mail(
                'You are flying in the next 24hours',
                msg_plain,
                settings.EMAIL_HOST_USER,
                [email],
                html_message=msg_html,
            )

            with transaction.atomic():
                passenger.flight.reminder_notification_sent_at = datetime.now().replace(tzinfo=pytz.UTC)
                passenger.flight.save()
