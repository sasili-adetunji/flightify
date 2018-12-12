from apps.files.serializers import FileSerializer
from django.urls import reverse_lazy
from django.db import transaction
from apps.ticket.models import Ticket
from django.conf import settings
from rest_framework.generics import get_object_or_404


def create_tickets(requestor):
    return 'None'
