import pytest

from apps.user.logic.selectors.user import user__find_by_pk


@pytest.mark.django_db()
def test__user__find_by_pk__success_case(user_factory):
    user = user_factory()
    user_result = user__find_by_pk(pk=user.pk)
    assert user == user_result
