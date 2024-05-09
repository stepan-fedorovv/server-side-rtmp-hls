import jwt
import pytest
from django.conf import settings

from apps.user.logic.interactors.user import user__generate_stream_key


@pytest.mark.django_db()
def test__generate_stream_key__success_case(user_factory):
    user = user_factory(
        email='some_email@example.com',
        username='some_username'
    )
    key = user__generate_stream_key(user=user)
    stream_key = key.split('_')[1]
    user_payload = jwt.decode(
        jwt=stream_key,
        key=settings.STREAM_KEY,
        algorithms=['HS256']
    )
    assert user_payload.get('email') == user.email
    assert user_payload.get('username') == user.username