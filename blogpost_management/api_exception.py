from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class TokenRequired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Token Required."
    default_code = 'token_required'


class InvalidSignature(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid token."
    default_code = 'invalid_token'


class ExpiredSignature(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Token is expired"
    default_code = 'not_authenticated'


class KeyRequired(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid internal call."
    default_code = 'invalid_internal_call'


class InvalidToken(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid token."
    default_code = 'invalid_token'


class InvalidTenant(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid tenant."
    default_code = 'invalid_tenant'


class ResourceDoesNotExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Resource does not exist."
    default_code = 'resource_not_exists'


class InternalCallException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Internal call failed."
    default_code = 'internal_call_failed'


class IssuerException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid issuer url."
    default_code = 'invalid_issuer_url'


class InvalidSession(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid session."
    default_code = 'invalid_session'


class StandardizedException(APIException):

    def __init__(self, error_status=True, error_obj: object = None,
                 status_code=status.HTTP_400_BAD_REQUEST):
        message = str(error_obj)
        if error_obj is not None:
            try:
                keys = list(error_obj.__dict__.keys())
                if len(keys):
                    message = error_obj.__dict__[keys[0]]
                    if len(message.keys()):
                        message = list(message.keys())[0] + ': ' + message[list(message.keys())[0]][0]
            except Exception:
                message = str(error_obj)
        default_detail = {'error': error_status, 'message': message}
        self.detail = default_detail
        self.default_code = message
        self.status_code = status_code


def custom_exception_handler(exc, context):
    """Custom EXCEPTION Handler"""
    response = exception_handler(exc, context)

    if response is not None and isinstance(response.data, dict):
        # Ensure boolean values remain booleans
        for key, value in response.data.items():
            if isinstance(value, str):
                if value.lower() == 'true':
                    response.data[key] = True
                elif value.lower() == 'false':
                    response.data[key] = False

    return response
