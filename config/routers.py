from rest_framework.routers import DefaultRouter

from apps.user.api.viewsets import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet)

