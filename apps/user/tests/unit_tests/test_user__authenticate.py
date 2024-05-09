from unittest import mock

import pytest
from django.contrib.auth.hashers import make_password

from apps.user.dto.authenticate import LoginDto
from apps.user.logic.interactors.user import user__authenticate
from utils.exeption import BusinessLogicException


@pytest.mark.django_db()
def test__user__authenticate__success_case(user_factory):
    user = user_factory(
        username="test_user2",
        password=make_password('password')
    )
    login_dto = LoginDto(
        username=user.username,
        password=user.password
    )
    with pytest.raises(BusinessLogicException):
        user__authenticate(login_dto=login_dto)
