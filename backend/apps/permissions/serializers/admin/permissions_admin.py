"""Admin: Rollar, permissionlar va endpointlar."""
from rest_framework import serializers

from apps.permissions.models.permissions import Endpoint, Permission, Role


class PermissionAdminSerializer(serializers.ModelSerializer):
    role_count = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'description', 'parent', 'role_count']

    def get_role_count(self, obj) -> int:
        return obj.roles.count() if hasattr(obj, 'roles') else 0


class RoleAdminSerializer(serializers.ModelSerializer):
    permission_ids = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()
    codename = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = [
            'id', 'name', 'codename', 'description',
            'permission_ids', 'user_count',
            'is_active',
        ]

    def get_permission_ids(self, obj) -> list[int]:
        return list(obj.permissions.values_list('id', flat=True))

    def get_user_count(self, obj) -> int:
        return obj.users.count() if hasattr(obj, 'users') else 0

    def get_codename(self, obj) -> str:
        return obj.name.lower().replace(' ', '_')


class RoleAdminUpdateSerializer(serializers.ModelSerializer):
    """Rol tahriri — permission ID'lari orqali M2M yangilash."""
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Role
        fields = ['name', 'description', 'is_active', 'permission_ids']

    def update(self, instance, validated_data):
        permission_ids = validated_data.pop('permission_ids', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if permission_ids is not None:
            instance.permissions.set(permission_ids)
        return instance


class EndpointAdminSerializer(serializers.ModelSerializer):
    required_permission = serializers.SerializerMethodField()

    class Meta:
        model = Endpoint
        fields = [
            'id',
            'path', 'method',
            'name', 'description',
            'access_type',
            'required_permission',
            'is_active',
        ]

    def get_required_permission(self, obj) -> str | None:
        return obj.permission.codename if obj.permission else None
