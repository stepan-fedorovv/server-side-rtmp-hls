import pytest

from apps.user.logic.selectors.user import user__all


@pytest.mark.django_db()
def test__user__all__success_case(user_factory):
    users = [user_factory() for _ in range(10)]
    users_result = user__all()
    assert len(users_result) == len(users)
