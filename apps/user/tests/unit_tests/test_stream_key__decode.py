import pytest

from apps.user.logic.interactors.stream_key import stream_key__decode
from apps.user.logic.interactors.user import user__generate_stream_key


@pytest.mark.django_db()
def test__stream_key__decode__success_case(user_factory):
    user = user_factory(
        email='test@example.com',
        username='test_test'
    )
    key = user__generate_stream_key(user=user)
    is_user_exists = stream_key__decode(key=key)
    assert is_user_exists is True
