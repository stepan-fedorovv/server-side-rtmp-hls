import typing

from django.db.models import QuerySet
from rest_framework.serializers import Serializer, ListSerializer

from utils.dto import DjangoModel
from utils.report import ReportGeneration, LoadFromExcelReport


class EXSLSerializer(Serializer, ReportGeneration, LoadFromExcelReport):

    def __init__(
            self, model: DjangoModel, filename: str | None = None, filepath: str | None = None, **kwargs: typing.Any
    ) -> None:
        self.queryset: QuerySet = model
        self.model = model
        self.filename = filename
        self.filepath = filepath
        super().__init__(**kwargs)

    class Meta:
        fields: list[tuple[str, str]] = []
        sheet_name = 'Sheet'
        filename = ''
        unique_fields = []

    def data(self) -> None:
        self.generate_report_for_sheet(
            sheet_name=self.Meta.sheet_name,
            fields=self.Meta.fields,
            filename=self.Meta.filename
        )

    def save(self, **kwargs: typing.Any) -> None:
        self.unloading_content_from_file(
            model=self.model,
            unique_fields=self.Meta.unique_fields,
            filepath=self.filepath,
            sheet=self.Meta.sheet_name
        )
