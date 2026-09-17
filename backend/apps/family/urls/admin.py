"""Family admin URL'lari."""
from django.urls import path

from apps.family.views.admin import FamilyAdminDetailAPIView, FamilyAdminListAPIView

app_name = 'family-admin'

urlpatterns = [
    path('', FamilyAdminListAPIView.as_view(), name='list'),
    path('<int:family_id>/', FamilyAdminDetailAPIView.as_view(), name='detail'),
]
