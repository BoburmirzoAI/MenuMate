from django.urls import path

from apps.family.views.family_member import (
    FamilyMemberDetailAPIView,
    FamilyMemberListCreateAPIView,
)
from apps.family.views.family_profile import FamilyProfileAPIView
from apps.family.views.health_condition import HealthConditionListAPIView

app_name = 'family'

urlpatterns = [
    # --- Family profile ---
    path('', FamilyProfileAPIView.as_view(), name='profile'),

    # --- Family members ---
    path('members/', FamilyMemberListCreateAPIView.as_view(), name='member-list-create'),
    path('members/<int:member_id>/', FamilyMemberDetailAPIView.as_view(), name='member-detail'),

    # --- Reference data ---
    path('health-conditions/', HealthConditionListAPIView.as_view(), name='health-conditions'),
]
