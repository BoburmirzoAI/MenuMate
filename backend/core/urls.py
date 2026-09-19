"""URL configuration for Menu Mate project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.shared.utils.decorators import superuser_required


_docs_view = SpectacularSwaggerView.as_view(url_name='schema')
_redoc_view = SpectacularRedocView.as_view(url_name='schema')
_docs_gate = (lambda v: v) if settings.DEBUG else superuser_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls.v1', namespace='v1')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', _docs_gate(_docs_view), name='swagger-ui'),
    path('api/v1/redoc/', _docs_gate(_redoc_view), name='redoc'),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
