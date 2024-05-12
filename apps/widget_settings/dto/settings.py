from utils.dto import BaseDto


class SettingsDto(BaseDto):
    width: int | None
    height: int | None
    avatar: bool | None
    is_username: bool | None
    username: str | None
    is_short_description: bool | None
    short_description: str | None
    is_description: bool | None
    description: str | None
