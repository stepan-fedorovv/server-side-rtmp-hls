from rest_framework.routers import DefaultRouter

from apps.user.api.viewsets import UserViewSet
from apps.widget_settings.api.viewsets import WidgetSettingsViewSet

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('widgets', WidgetSettingsViewSet)



