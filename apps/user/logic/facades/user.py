from apps.user.dto.authenticate import RegistrationDto
from apps.user.logic.interactors.user import user__create, user__generate_stream_key
from apps.user.models import User


def user__registration(*, validated_data: RegistrationDto) -> tuple[User, str]:
    user = user__create(validated_data=validated_data)
    stream_key = user__generate_stream_key(user=user)
    return user, stream_key
