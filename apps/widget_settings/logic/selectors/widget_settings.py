from django.db.models import QuerySet

from apps.user.models import User
from apps.widget_settings.models import WidgetSettings


def widget_settings__all():
    return WidgetSettings.objects.all()


def widget_settings__find_by_user(
        user: User,
        queryset: QuerySet[WidgetSettings] | None = None
) -> WidgetSettings:
    if not queryset:
        queryset = widget_settings__all()
    return queryset.filter(user=user).first()


def widget_settings__find_by_user_and_code(
        user: User,
        code: str,
        queryset: QuerySet[WidgetSettings] | None = None
) -> WidgetSettings:
    if not queryset:
        queryset = widget_settings__all()
    return queryset.filter(user=user, code=code).first()
