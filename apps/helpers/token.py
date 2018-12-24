import itsdangerous

from django.conf import settings


def generate_confirmation_token(email):
    """ function that generate confrimation token from email"""

    serializer = itsdangerous.URLSafeTimedSerializer(settings.SECRET_KEY)

    return serializer.dumps(email, salt=settings.SECURITY_PASSWORD_SALT)


def confirm_token(token, expiration=3600):
    """ function that decode email from token """

    serializer = itsdangerous.URLSafeTimedSerializer(settings.SECRET_KEY)

    try:
        email = serializer.loads(
            token,
            salt=settings.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
