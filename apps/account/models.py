from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    def get_full_name(self):
        """ Returns formatted users full name """
        return '{} {}'.format(self.first_name, self.last_name)
    # pass