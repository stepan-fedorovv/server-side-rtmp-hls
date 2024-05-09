import pytest

from apps.user.logic.selectors.user import user__exists, user__find_by_username


@pytest.mark.django_db()
def test__user__exists__success_case(user_factory):
    user = user_factory()
    user = user__find_by_username(
        username=user.username
    )
    user_exists = user__exists(
        queryset=user
    )
    assert user_exists is True
