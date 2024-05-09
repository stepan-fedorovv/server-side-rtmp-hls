import typing

from django.core.validators import (FileExtensionValidator,
                                    get_available_image_extensions)
from django.db.models import FileField, Model
from django.utils.safestring import mark_safe


def validate_image_or_svg_file_extension(value: str) -> FileExtensionValidator:
    allowed_extensions = get_available_image_extensions() + ["svg"]
    return FileExtensionValidator(allowed_extensions=allowed_extensions)(value)


class ImageOrSVGField(FileField):
    default_validators = [validate_image_or_svg_file_extension]

    def pre_save(self, model_instance: Model, add: typing.Any) -> super:
        return super().pre_save(model_instance=model_instance, add=add)
