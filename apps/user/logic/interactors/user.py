import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from apps.user.models import User

from apps.user.dto.authenticate import RegistrationDto, LoginDto
from utils.exeption import BusinessLogicException


def user__create(*, validated_data: RegistrationDto) -> User:
    username = validated_data.username
    password = validated_data.password
    email = validated_data.email
    re_password = validated_data.re_password
    if password != re_password:
        raise BusinessLogicException('Пароли не совпадают')
    hashed_password = make_password(password)
    user = User.objects.create(username=username, password=hashed_password)
    return user


def user__generate_stream_key(*, user: User) -> str:
    stream_key = "stream_" + jwt.encode(
        payload={'username': user.username, 'email': user.email},
        key=settings.STREAM_KEY,
        algorithm='HS256',
    )
    return stream_key


def user__authenticate(login_dto: LoginDto):
    user = authenticate(
        username=login_dto.username,
        password=login_dto.password
    )
    if not user:
        raise BusinessLogicException('Пользователь не найден')
    return user

