from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from restdoctor.rest_framework import viewsets
from silk.profiling.profiler import silk_profile

from apps.widget_settings.api.serializers import WidgetSettingsSerializer, WidgetSettingsPydanticSerializer
from apps.widget_settings.dto.settings import SettingsDto
from apps.widget_settings.logic.facades.widget_settings import create_widget_settings
from apps.widget_settings.logic.selectors.widget_settings import widget_settings__find_by_user_and_code
from apps.widget_settings.models import WidgetSettings
from utils.exeption import BusinessLogicException


class WidgetSettingsViewSet(viewsets.ModelViewSet):
    queryset = WidgetSettings.objects.all()
    serializer_class_map = {
        'default': WidgetSettingsSerializer,
        'save_settings': {
            'request': WidgetSettingsPydanticSerializer
        },
        'get_settings': {
            'response': WidgetSettingsPydanticSerializer
        }
    }
    permission_classes_map = {
        'default': [permissions.IsAuthenticated, ]
    }

    @action(detail=False, methods=['post'])
    def save_settings(self, request: Request) -> Response:
        request_serializer = self.get_request_serializer(
            data=request.data
        )
        request_serializer.is_valid(raise_exception=True)
        code = create_widget_settings(
            user=request.user,
            settings_dto=request_serializer.pydantic_instance
        )

        return Response(data={'code': code}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def get_settings(self, request: Request) -> Response:
        user = request.user
        code = request.query_params.get('code')
        settings = widget_settings__find_by_user_and_code(
            user=user,
            code=code
        )
        if settings is None:
            raise BusinessLogicException('Настройки не найдены')
        response_serializer = self.get_response_serializer(
            instance=SettingsDto(**settings.settings.dict())
        )
        return Response(response_serializer.data)
