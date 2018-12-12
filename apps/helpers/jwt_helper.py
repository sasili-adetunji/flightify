from calendar import timegm
from rest_framework_jwt.settings import api_settings
from datetime import datetime

def jwt_payload_handler(user):
    """ Custom payload handler
    Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        'iss': 'flightify',
        'username': user.username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'iat': timegm(datetime.utcnow().utctimetuple())
    }
  