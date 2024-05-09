import typing

from django.db import models
from solo.models import SingletonModel


class AbstractBaseModel(models.Model):
    """
    Base class from which all models should be inherited,
    in order to have an option to add behavior to the group of models
    """

    class Meta:
        abstract = True

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: typing.Any | None = None,
            update_fields: typing.Any | None = None,
    ) -> None:
        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class AbstractBaseSoloModel(SingletonModel):
    """
    Base class from which all models should be inherited,
    in order to have an option to add behavior to the group of models
    """

    class Meta:
        abstract = True

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: typing.Any | None = None,
            update_fields: typing.Any | None = None,
    ) -> None:
        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )


class AbstractModelWithSerialNumberAsPK(models.Model):
    serial_number = models.CharField(
        max_length=255,
        primary_key=True,
        editable=False,
        verbose_name='Серийный номер',
        help_text='Указывает на серийный номер'
    )

    class Meta:
        abstract = True

    def save(
            self,
            force_insert: bool = False,
            force_update: bool = False,
            using: typing.Any | None = None,
            update_fields: typing.Any | None = None,
    ) -> None:
        self.full_clean()
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )
