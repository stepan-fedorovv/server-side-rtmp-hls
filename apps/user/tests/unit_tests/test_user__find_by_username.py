import pytest

from apps.user.logic.selectors.user import user__find_by_username


@pytest.mark.django_db()
def test__user__find_by_username__success_case(user_factory):
    user = user_factory()
    user_result = user__find_by_username(
        username=user.username
    )
    assert user_result.first() == user
