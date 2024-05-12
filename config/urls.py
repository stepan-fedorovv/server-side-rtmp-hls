from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from config.routers import router
from django.conf.urls.static import static

from config.yasg import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
if settings.DEBUG:
    urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
