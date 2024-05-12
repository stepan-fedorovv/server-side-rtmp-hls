from python_random_strings import random_strings

from apps.user.models import User
from apps.widget_settings.dto.settings import SettingsDto
from apps.widget_settings.logic.selectors.widget_settings import widget_settings__find_by_user
from apps.widget_settings.models import WidgetSettings


def create_widget_settings(
        *,
        user: User,
        settings_dto: SettingsDto
):
    widget = widget_settings__find_by_user(
        user=user
    )
    if widget is None:
        widget, created = WidgetSettings.objects.update_or_create(
            settings=settings_dto.dict(),
            user=user
        )
        if created:
            widget.code = random_strings.random_letters(20)
            widget.save()

    return widget.code
