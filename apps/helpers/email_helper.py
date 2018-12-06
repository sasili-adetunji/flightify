# from apps.helpers.token import generate_confirmation_token
# from django.core.mail import send_mail
from django.conf import settings

# def send_signup_confirmation(email, data):
#     link="/activate/{}".format(generate_confirmation_token(email))
#     send_mail(
#         'Email Confirmation',
#         'Please confirm the link {}'.format(link),
#         settings.EMAIL_TO,
#         [email],
#         fail_silently=False,
#     )
