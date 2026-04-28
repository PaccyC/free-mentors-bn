import jwt
import datetime
from django.conf import settings


def _jwt_secret():
    return getattr(settings, 'JWT_SECRET', None) or settings.SECRET_KEY


def create_token(user):
    payload = {
        'user_id': str(user.id),
        'email': user.email,
        'role': user.role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm='HS256')


def decode_token(token):
    return jwt.decode(token, _jwt_secret(), algorithms=['HS256'])


def get_user_from_info(info):
    """Extract JWT from request and return the matching User, or None."""
    from users.models import User
    auth = info.context.META.get('HTTP_AUTHORIZATION', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth.split(' ', 1)[1]
    try:
        payload = decode_token(token)
        # Look up by email — avoids ObjectId string-to-BSON conversion issues
        return User.objects.get(email=payload['email'])
    except Exception:
        return None
