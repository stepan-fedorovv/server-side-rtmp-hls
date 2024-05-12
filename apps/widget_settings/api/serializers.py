from apps.widget_settings.models import WidgetSettings
from utils.abstractions.serializer import PydanticSerializer, AbstractModelSerializer
from apps.widget_settings.dto.settings import SettingsDto


class WidgetSettingsSerializer(AbstractModelSerializer):
    class Meta:
        model = WidgetSettings
        fields = '__all__'


class WidgetSettingsPydanticSerializer(PydanticSerializer):
    class Meta:
        pydantic_model = SettingsDto
