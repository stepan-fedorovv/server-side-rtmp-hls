from utils.dto import BaseDto


class RegistrationDto(BaseDto):
    username: str
    password: str
    email: str
    re_password: str


class LoginDto(BaseDto):
    username: str
    password: str
