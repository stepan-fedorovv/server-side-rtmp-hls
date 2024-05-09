import jwt
from django.conf import settings

from apps.user.logic.selectors.user import user__find_by_username, user__exists


def stream_key__decode(key):
    stream_key = key.split('_')[1]
    user_payload = jwt.decode(
        jwt=stream_key,
        key=settings.STREAM_KEY,
        algorithms=['HS256']
    )
    user = user__find_by_username(username=user_payload.get('username'))
    is_user_exists = user__exists(queryset=user)
    return is_user_exists
