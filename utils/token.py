# utils/token.py
import uuid

import jwt
from datetime import datetime, timedelta
from django.conf import settings


# def create_token(user_id, email, expires_in_hours=2):
#     """
#     Generates a simple JWT access token with custom claims.
#     No refresh token is returned.
#     """
#
#     payload = {
#         'user_id': str(user_id),
#         'email': email,
#         'exp': datetime.now()+ timedelta(hours=expires_in_hours),
#         'iat': datetime.now()
#     }
#
#     token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
#
#     return token

def create_token(user_id, email, expires_in_hours=2):
    """
    Generates a JWT access token compatible with SimpleJWT.
    """
    now = datetime.utcnow()
    exp = now + timedelta(hours=expires_in_hours)

    payload = {
        "token_type": "access",
        "jti": str(uuid.uuid4()),  # unique token identifier
        "user_id": str(user_id),   # use int if not UUID
        "email": email,
        "iat": int(now.timestamp()),  # issued at
        "exp": int(exp.timestamp()),  # expiry
    }

    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token
