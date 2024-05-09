import datetime
import typing

import pgbulk
from django.db.models import ForeignKey, QuerySet, ManyToOneRel
from openpyexcel import Workbook, load_workbook
from openpyexcel.styles import Alignment, Font, NamedStyle
from openpyexcel.utils import get_column_letter
from openpyexcel.worksheet import Worksheet

from utils.dto import DjangoModel


class ReportGeneration:
    def __init__(self, model: DjangoModel) -> None:
        self.model: DjangoModel = model
        self.sheet_name: str = ''

    @property
    def _default_styles(self: typing.Any) -> dict[str, typing.Any]:
        return {
            'bold': NamedStyle(name='bold', font=Font(b=True)),
            'header_style': NamedStyle(
                name='header_style',
                font=Font(b=True),
                alignment=Alignment(horizontal='center', vertical='center', wrap_text=True),
            ),
            'alignment': NamedStyle(
                name='alignment',
                alignment=Alignment(horizontal='center', vertical='center'),
            )
        }

    def generate_report_for_sheet(
            self: typing.Any, filename: str, sheet_name: str, fields: list[tuple[str, str]]
    ) -> None:
        workbook = self._get_base_workbook()
        sheet = self._set_sheet_name(workbook=workbook, sheet_name=sheet_name)
        header_fields = [self.model._meta.get_field(field).verbose_name for field in fields]
        self._set_header(sheet=sheet, fields=header_fields)
        value_list = self._change_fields_representation(model=self.model, value_list=fields)
        self._set_column_width(sheet=sheet, count_of_columns=len(value_list), value_list=value_list)
        self._set_cells(value_list=value_list, sheet=sheet)
        workbook.save(filename=filename)

    def _set_header(self: typing.Any, sheet: Worksheet, fields: list[str]) -> None:
        for key, field in enumerate(fields, 1):
            sheet.cell(row=1, column=key).value = field
            column_letter = get_column_letter(key)
            sheet[f"{column_letter}1"].style = 'header_style'

    def _change_fields_representation(
            self: typing.Any, model: DjangoModel, value_list: list[str]
    ) -> list[dict[str, typing.Any]]:
        queryset: QuerySet = model.objects.all()
        queryset_values: list[dict[str, str]] = queryset.values(*value_list)
        fields: list[typing.Any] = [model._meta.get_field(i) for i in value_list]
        fields_to_representation = self._get_fields_to_representations(fields=fields)
        representation_values: list[dict[str, str]] = []

        for key, queryset_obj in enumerate(queryset):
            value = queryset_values[key]
            for fields in fields_to_representation:
                if fields[0] == 'choices':
                    value[fields[1]] = getattr(queryset_obj, f'get_{fields[1]}_display')()
                elif fields[0] == 'foreign_key':
                    value[fields[1]] = getattr(queryset_obj, f'{fields[1]}').__repr__()
            representation_values.append(value)

        return representation_values

    def _get_fields_to_representations(self: typing.Any, fields: list[typing.Any]) -> list[tuple[str, typing.Any]]:
        fields_to_representation = []
        for value in fields:
            if getattr(value, 'choices') is not None:
                fields_to_representation.append(('choices', value.name))
            if isinstance(value, ForeignKey):
                fields_to_representation.append(('foreign_key', value.name))
        return fields_to_representation

    def _set_cells(self: typing.Any, sheet: Worksheet, value_list: list[dict[str, str]]) -> None:
        row = 1
        for value_obj in value_list:
            row += 1
            for key, value in enumerate(value_obj, 1):
                sheet.cell(row=row, column=key).value = value_obj[value]
                column_letter = get_column_letter(key)
                sheet[f'{column_letter}{row}'].style = 'alignment'
                if type(value_obj[value]) is datetime.datetime:
                    sheet[f'{column_letter}{row}'].number_format = 'DD MMM YYYY'

    def _set_column_width(
            self, sheet: Worksheet, count_of_columns: int, value_list: list[dict[str, typing.Any]]
    ) -> None:
        letters = []
        for column in range(1, count_of_columns + 1):
            column_letter = get_column_letter(column)
            letters.append(column_letter)
        columns_width = {key: max(len(str(value[key])) for value in value_list) for key in value_list[0].keys()}
        for key, letter in enumerate(letters):
            sheet.column_dimensions[letter].width = (list(columns_width.values())[key] + 2) * 1.2

    def _get_base_workbook(self: typing.Any) -> Workbook:
        workbook = Workbook()
        workbook.remove_sheet(workbook['Sheet'])
        self._fill_workplace_style(workbook=workbook)
        return workbook

    @property
    def styles(self) -> dict[str, typing.Any]:
        return self._default_styles

    def _set_sheet_name(self: typing.Any, workbook: Workbook, sheet_name: str) -> Worksheet:
        self.sheet_name = sheet_name
        workbook_sheet = workbook.create_sheet(title=self.sheet_name)
        return workbook_sheet

    def _fill_workplace_style(self: typing.Any, workbook: Workbook) -> None:
        for _, style in self.styles.items():
            workbook.add_named_style(style)


class LoadFromExcelReport:

    def unloading_content_from_file(
            self: typing.Any, model, filepath: str, unique_fields, sheet: str
    ) -> None:
        workbook = self._load_workbook(filepath=filepath)
        worksheet = workbook[sheet]
        header_values = self._collect_header_values(worksheet=worksheet)
        model_fields, verbose_names = self._match_header_values_and_model_fields_by_verbose_name(
            header_values=header_values,
            model=model
        )
        model_fields_and_value_array = self._generate_model_fields_and_value_map(
            worksheet=worksheet,
            model_fields=model_fields,
            verbose_names=verbose_names
        )
        model_objects = self._generate_array_of_model_objects(
            fields_value_of_model=model_fields_and_value_array,
            model=model
        )
        self._create_or_update_model_fields(
            model=model,
            model_objects=model_objects,
            unique_fields=unique_fields
        )


    def _create_or_update_model_fields(
            self, model, model_objects, unique_fields: list[str]
    ) -> None:
        pgbulk.upsert(
            queryset=model,
            model_objs=model_objects,
            unique_fields=unique_fields
        )

    def _match_header_values_and_model_fields_by_verbose_name(
            self,
            header_values: list[str],
            model
    ) -> tuple[list[str], list[str]]:
        fields = model._meta.get_fields()
        model_fields_verbose_name = [
            field.verbose_name for field in fields if not isinstance(field, ManyToOneRel)
        ]
        actual_fields = []
        for key, value in enumerate(header_values):
            if value in model_fields_verbose_name:
                actual_fields.append(
                    *[
                        field.name for field in fields if
                        not isinstance(field, ManyToOneRel) and field.verbose_name == value
                    ]
                )
        return actual_fields, model_fields_verbose_name

    def _generate_model_fields_and_value_map(
            self,
            worksheet: Worksheet,
            model_fields: list[str],
            verbose_names: list[str]
    ) -> list[dict[str, str]]:
        model_fields_values = []
        for row in range(worksheet.max_row):
            model_fields_map = {}
            for column in range(worksheet.max_column):
                cell_value = worksheet.cell(row=row + 1, column=column + 1).value

                if cell_value not in verbose_names:
                    model_fields_map[
                        model_fields[column]
                    ] = worksheet.cell(row=row + 1, column=column + 1).value
            if model_fields_map:
                model_fields_values.append(model_fields_map)

        return model_fields_values

    def _generate_array_of_model_objects(
            self,
            model,
            fields_value_of_model: list[dict[str, str]]
    ) -> list:
        models_objects = [model(**i) for i in fields_value_of_model]
        return models_objects

    def _collect_header_values(
            self,
            worksheet: Worksheet
    ) -> list[str]:
        header_values = []
        for column in range(1, worksheet.max_column + 1):
            header_values.append(worksheet.cell(row=1, column=column).value)
        return header_values

    def _load_workbook(self, filepath: str) -> Workbook:
        workbook = load_workbook(filepath)
        return workbook
