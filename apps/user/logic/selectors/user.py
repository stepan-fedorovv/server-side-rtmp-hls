from django.db.models import QuerySet

from apps.user.models import User


def user__all():
    return User.objects.all()


def user__find_by_pk(pk: int, queryset: QuerySet[User] | None = None) -> User:
    if queryset is None:
        queryset = user__all()
    return queryset.filter(pk=pk).first()


def user__find_by_username(username: str, queryset: QuerySet[User] | None = None) -> QuerySet[User]:
    if queryset is None:
        queryset = user__all()
    return queryset.filter(username=username)


def user__exists(queryset: QuerySet[User]) -> bool:
    if queryset is None:
        queryset = user__all()
    return queryset.exists()
