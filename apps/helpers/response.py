
from rest_framework.response import Response

class APIResponse(Response):

    ''' Custom API response '''

    def __init__(self, data, **kwargs):

        data = {
            'payload': data,
            'message': kwargs.pop('message', None),
            'success': True,
        }

        super(APIResponse, self).__init__(data, **kwargs)
