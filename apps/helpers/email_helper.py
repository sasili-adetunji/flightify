from apps.helpers.token import generate_confirmation_token
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site



def send_signup_confirmation(user):

    site = Site.objects.first()
    site_domain = site.domain
    link=generate_confirmation_token(user['email'])
    msg_plain = render_to_string('account/confirm_signup.txt', {'user': user, 'link': link, 'site': site_domain})
    msg_html = render_to_string('account/confirm_signup.html', {'user': user, 'link': link, 'site': site_domain})

    send_mail(
        'Email confirmation on Flightify',
        msg_plain,
        settings.EMAIL_HOST_USER,
        [user['email']],
        html_message=msg_html,
    )