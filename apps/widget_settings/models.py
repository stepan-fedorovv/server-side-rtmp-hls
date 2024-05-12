from django.db import models
import django_pydantic_field

from apps.widget_settings.dto.settings import SettingsDto
from utils.abstractions.model import AbstractBaseModel
from apps.user.models import User


class WidgetSettings(AbstractBaseModel):
    class Meta:
        verbose_name = 'Настройки виджета'
        verbose_name_plural = 'Настройки виджета'

    settings: SettingsDto = django_pydantic_field.SchemaField(
        verbose_name='Настройки окна траснляции',
        help_text='Настройки окна траснляции'
    )
    user = models.ForeignKey(
        to=User,
        verbose_name='Пользователь',
        help_text='Пользователь',
        on_delete=models.CASCADE
    )
    code = models.CharField(
        max_length=255,
        verbose_name='Ключ настроек',
        help_text='Ключ настроек',
        blank=True,
        null=True
    )
