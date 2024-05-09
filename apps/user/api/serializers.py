from apps.user.models import User
from restdoctor.rest_framework.serializers import PydanticSerializer

from apps.user.dto.authenticate import RegistrationDto, LoginDto
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class RegistrationSerializer(PydanticSerializer):
    class Meta:
        pydantic_model = RegistrationDto


class LoginSerializer(PydanticSerializer):
    class Meta:
        pydantic_model = LoginDto
