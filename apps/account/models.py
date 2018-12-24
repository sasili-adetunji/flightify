from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def get_full_name(self):
        """ Returns formatted users full name """
        return '{} {}'.format(self.first_name, self.last_name)
