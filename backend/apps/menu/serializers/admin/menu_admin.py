"""Admin: menyular ro'yxati va tafsilotlari."""
from rest_framework import serializers

from apps.menu.models.menu import Menu


class MenuAdminListSerializer(serializers.ModelSerializer):
    family_name = serializers.CharField(source='family.family_name', read_only=True)
    owner_email = serializers.CharField(source='family.user.email', read_only=True)

    class Meta:
        model = Menu
        fields = [
            'id',
            'family', 'family_name', 'owner_email',
            'start_date', 'end_date',
            'duration', 'status',
            'notes',
            'created_at',
        ]


class MenuAdminDetailSerializer(MenuAdminListSerializer):
    class Meta(MenuAdminListSerializer.Meta):
        pass
