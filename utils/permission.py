import jwt
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from user_management.models import Users


class IsAuthenticatedWithSimpleToken(BasePermission):
    """
    Custom permission to check if a valid simple JWT token is present in the Authorization header.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Authorization header missing or improperly formatted.")

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token has expired.")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token.")

        try:
            user = Users.objects.get(id=payload['user_id'], email_id=payload['email'])
        except Users.DoesNotExist:
            raise AuthenticationFailed("User not found.")

        # Attach user to request if needed
        request.user = user
        return True
