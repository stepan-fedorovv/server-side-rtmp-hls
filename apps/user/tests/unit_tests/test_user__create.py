import pytest

from apps.user.dto.authenticate import RegistrationDto
from apps.user.logic.interactors.user import user__create
from utils.exeption import BusinessLogicException


@pytest.mark.django_db()
def test__user__create__success_case():
    dto = RegistrationDto(
        email='test_email@example.com',
        username='test',
        password='testTest',
        re_password='testTest',
    )
    user__create(validated_data=dto)


@pytest.mark.django_db()
def test__user__create__error_case():
    dto = RegistrationDto(
        email='test_email@example.com',
        username='test',
        password='testTest',
        re_password='testTest1',
    )
    with pytest.raises(BusinessLogicException):
        user__create(validated_data=dto)
