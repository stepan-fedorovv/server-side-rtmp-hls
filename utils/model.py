import traceback
from contextlib import suppress
from typing import Tuple, Type

from django.db.models import DateField, DateTimeField, Field, Model, TimeField
from rest_framework.utils import model_meta
from restdoctor.utils.custom_types import GenericContext

from utils.dto import DjangoModel


def get_all_fields_names(*, model: type[Model]) -> list[str]:
    return [field.name for field in model._meta.fields]


def get_updated_fields(*, model: type[Model], data: dict) -> dict:
    return {
        element: data.get(element)
        for element in filter(lambda field: field in get_all_fields_names(model=model), data)
    }


def model_update(*, instance: Model, updated_fields: dict) -> None:
    for key, value in updated_fields.items():
        setattr(instance, key, value)
    instance.save()


def field__is_auto_now(*, field: Field) -> bool:
    return isinstance(field, (DateField, DateTimeField, TimeField)) and getattr(
        field, "auto_now", False
    )


def update_model_instance_suppressed(  # noqa: CAC001 because used DRF realisation
    *,
    instance: DjangoModel,
    validated_data: GenericContext,
    update_fields: list[str] | None = None,
) -> DjangoModel:
    info = model_meta.get_field_info(instance)
    model_fields = instance.__class__._meta.fields
    auto_fields = [field.attname for field in model_fields if field__is_auto_now(field=field)]
    # Simply set each attribute on the instance, and then save it.
    # Note that unlike `create_model_instance()` we don't need to treat many-to-many
    # relationships as being a special case. During updates we already
    # have an instance pk for the relationships to be associated with.
    m2m_fields = []
    common_fields = []
    for attr, value in validated_data.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))
        else:
            setattr(instance, attr, value)
            common_fields.append(attr)
    update_fields = update_fields or common_fields
    update_fields += auto_fields
    instance.save(update_fields=update_fields)
    # Note that many-to-many fields are set after updating instance.
    # Setting m2m fields triggers signals which could potentially change
    # updated instance and we do not want it to collide with update_model_instance()
    for attr, value in m2m_fields:
        field = getattr(instance, attr)
        field.set(value)
    return instance


def create_model_instance_suppressed(  # noqa: CAC001 because used DRF realisation
    *, model_class: Type[DjangoModel], validated_data: GenericContext
) -> DjangoModel:
    """
    We have a bit of extra checking around this in order to provide
    descriptive messages when something goes wrong, but this method is
    essentially just:

        return ExampleModel.objects.create(**validated_data)

    If there are many to many fields present on the instance then they
    cannot be set until the model is instantiated, in which case the
    implementation is like so:

        example_relationship = validated_data.pop('example_relationship')
        instance = ExampleModel.objects.create(**validated_data)
        instance.example_relationship = example_relationship
        return instance

    The default implementation also does not handle nested relationships.
    If you want to support writable nested relationships you'll need
    to write an explicit `create_model_instance()` method.
    """

    # Remove many-to-many relationships from validated_data.
    # They are not valid arguments to the default `.create()` method,
    # as they require that the instance has already been saved.
    info = model_meta.get_field_info(model_class)
    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    try:
        instance = model_class._default_manager.create(**validated_data)
    except TypeError:
        tb = traceback.format_exc()
        msg = (
            "Got a `TypeError` when calling `{model}.{manager}.create()`. "
            "This may be because you have a writable field on the "
            "serializer class that is not a valid argument to "
            "`{model}.{manager}.create()`.\nOriginal exception was:\n {traceback}".format(
                model=model_class.__name__, manager=model_class._default_manager.name, traceback=tb
            )
        )
        raise TypeError(msg)

    # Save many-to-many relationships after the instance is created.
    if many_to_many:
        for field_name, value in many_to_many.items():
            field = getattr(instance, field_name)
            field.set(value)

    return instance


def create_model_instance(
    model_class: Type[DjangoModel], validated_data: GenericContext, refresh: bool = False
) -> DjangoModel:
    instance = create_model_instance_suppressed(
        model_class=model_class, validated_data=validated_data
    )
    if refresh:
        instance.refresh_from_db()

    return instance


def update_model_instance(
    instance: DjangoModel,
    validated_data: GenericContext,
    refresh: bool = False,
    update_fields: list[str] | None = None,
) -> DjangoModel:
    instance = update_model_instance_suppressed(
        instance=instance, validated_data=validated_data, update_fields=update_fields
    )
    if refresh:
        instance.refresh_from_db()

    return instance


def create_or_update_model_instance(
    validated_data: GenericContext,
    model_class: Type[DjangoModel],
    refresh: bool = False,
    update_fields: list[str] | None = None,
) -> tuple[DjangoModel, bool]:
    with suppress(Exception):
        return (
            update_model_instance(
                instance=model_class(**validated_data),
                validated_data=validated_data,
                refresh=refresh,
                update_fields=update_fields,
            ),
            False,
        )
    return (
        create_model_instance(
            model_class=model_class, validated_data=validated_data, refresh=refresh
        ),
        True,
    )
