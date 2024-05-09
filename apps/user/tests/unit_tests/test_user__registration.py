import pytest

from apps.user.dto.authenticate import RegistrationDto
from apps.user.logic.facades.user import user__registration


@pytest.mark.django_db()
def test__user_registration__success_case():
    dto = RegistrationDto(
        username='test',
        email='test@example.com',
        password='testTest',
        re_password='testTest',
    )
    user__registration(
        validated_data=dto
    )

