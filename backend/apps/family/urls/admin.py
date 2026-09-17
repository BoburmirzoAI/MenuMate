"""Family admin URL'lari."""
from django.urls import path

from apps.family.views.admin import (
    FamilyAdminDetailAPIView,
    FamilyAdminListAPIView,
    FamilyMemberDetailAdminAPIView,
    FamilyMembersAdminListAPIView,
)

app_name = 'family-admin'

urlpatterns = [
    path('', FamilyAdminListAPIView.as_view(), name='list'),
    path('<int:family_id>/', FamilyAdminDetailAPIView.as_view(), name='detail'),
    path(
        '<int:family_id>/members/',
        FamilyMembersAdminListAPIView.as_view(),
        name='members-list',
    ),
    path(
        '<int:family_id>/members/<int:member_id>/',
        FamilyMemberDetailAdminAPIView.as_view(),
        name='members-detail',
    ),
]
