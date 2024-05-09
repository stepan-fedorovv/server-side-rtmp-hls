import typing

from django.conf import settings
from restdoctor.rest_framework.schema import generators, openapi


class CustomSchemaGenerator(generators.SchemaGenerator):
    def get_info(self) -> dict:
        info = {
            'title': settings.SWAGGER_UI_TITLE or '',
            'version': settings.SWAGGER_UI_VERSION or '',
            'description': settings.SWAGGER_UI_DESCRIPTION or ''
        }

        return info


class CustomRefsSchemaGenerator(CustomSchemaGenerator):
    def __init__(self, *args: typing.Any, **kwargs: typing.Any):
        super().__init__(*args, **kwargs)
