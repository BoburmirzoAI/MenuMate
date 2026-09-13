"""URL configuration for Menu Mate project."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularRedocView,
    SpectacularAPIView,
)

from apps.shared.utils.decorators import superuser_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.urls.v1', namespace='v1')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

schema_view = SpectacularSwaggerView.as_view(url_name='schema')
redoc_view = SpectacularRedocView.as_view(url_name='schema')

urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

if settings.DEBUG:
    urlpatterns += [
        path("api/v1/docs/", schema_view, name="swagger-ui"),
        path("api/v1/redoc/", redoc_view, name="redoc"),
    ]
else:
    urlpatterns += [
        path("api/v1/docs/", superuser_required(schema_view), name="swagger-ui"),
        path("api/v1/redoc/", superuser_required(redoc_view), name="redoc"),
    ]
