from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from apps.user.models import User
from utils.abstractions.admin import AbstractAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin, AbstractAdmin):
    fieldsets = (
        (
            _("General"),
            {
                "fields": (
                    "username",
                    "password"
                )
            }
        ),
        (
            _("Personal info"),
            {
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "avatar"
                )
            }
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Read only fields"),
            {
                "fields": (
                    "last_login",
                    "date_joined"
                )
            }
        ),
    )
    readonly_fields = (
        "last_login",
        "date_joined",
        "preview_avatar",
    )
    list_display = (
        'id',
        "username",
        "email",
        "is_staff",
        "last_login",
    )
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = (
        "is_staff",
        "is_active",
        "groups"
    )
    search_fields = (
        "username",
        "nickname"
    )
    ordering = ("date_joined",)

    @admin.display(description=_('Avatar Preview'))
    def preview_avatar(self, instance: User) -> str:
        if instance.avatar:
            return mark_safe(
                f'<img src="{instance.avatar.url}" style="height: 250px; border-radius: 8px"/>'
            )
        return ''

    @admin.display(description=_('Subscriptions count'))
    def subscriptions_count(self, instance: User) -> str:
        return instance.subscriptions.count()

    @admin.display(description=_('Subscribers count'))
    def subscribers_count(self, instance: User) -> str:
        return instance.subscribers.count()
