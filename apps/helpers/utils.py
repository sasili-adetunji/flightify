from apps.account.serializers import UserSerializer

def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(
            instance=user, context={'request': request}
        ).data
    }
