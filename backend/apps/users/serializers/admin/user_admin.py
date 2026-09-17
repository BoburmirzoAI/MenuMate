"""Admin panel uchun User serializer'lari."""
from rest_framework import serializers

from apps.users.models.users import User


class _RoleMiniSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    codename = serializers.CharField()


class UserAdminListSerializer(serializers.ModelSerializer):
    """Admin ro'yxati — jadval uchun asosiy maydonlar."""
    roles = serializers.SerializerMethodField()
    is_premium = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name', 'last_name',
            'phone_number',
            'gender', 'avatar',
            'timezone',
            'is_email_verified',
            'is_active',
            'is_onboarded',
            'is_premium',
            'roles',
            'created_at',
        ]

    def get_roles(self, obj) -> list:
        roles_qs = getattr(obj, 'roles', None)
        if roles_qs is None:
            return []
        return [
            {'id': r.id, 'name': r.name, 'codename': r.codename}
            for r in roles_qs.all()
        ]

    def get_is_premium(self, obj) -> bool:
        return bool(getattr(obj, 'is_premium', False))


class UserAdminDetailSerializer(UserAdminListSerializer):
    """Alohida foydalanuvchining to'liq tafsilotlari."""
    family_id = serializers.SerializerMethodField()
    devices_count = serializers.SerializerMethodField()

    class Meta(UserAdminListSerializer.Meta):
        fields = UserAdminListSerializer.Meta.fields + [
            'birth_date',
            'language',
            'is_push_enabled',
            'email_verified_at',
            'family_id',
            'devices_count',
        ]

    def get_family_id(self, obj) -> int | None:
        fam = getattr(obj, 'family_profile', None)
        return fam.id if fam else None

    def get_devices_count(self, obj) -> int:
        return obj.devices.count() if hasattr(obj, 'devices') else 0


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    """Admin PATCH: is_active toggle + role assignment (roles ID list)."""
    role_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True,
    )

    class Meta:
        model = User
        fields = ['is_active', 'is_email_verified', 'role_ids']

    def update(self, instance, validated_data):
        role_ids = validated_data.pop('role_ids', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if role_ids is not None:
            instance.roles.set(role_ids)
        return instance
