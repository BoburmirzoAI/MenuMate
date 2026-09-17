"""Admin panel uchun User serializer'lari."""
from rest_framework import serializers

from apps.users.models.users import User


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
            {'id': r.id, 'name': r.name, 'codename': r.name.lower().replace(' ', '_')}
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
        fam = getattr(obj, 'family_profile', None) or getattr(obj, 'family', None)
        return fam.id if fam else None

    def get_devices_count(self, obj) -> int:
        return obj.devices.count() if hasattr(obj, 'devices') else 0


class UserAdminCreateSerializer(serializers.ModelSerializer):
    """Yangi user yaratish — admin panel orqali.

    Superuser bo'lmagan admin foydalanuvchi qo'shishi mumkin. Parol majburiy.
    """
    password = serializers.CharField(write_only=True, min_length=6)
    role_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        default=list,
    )

    class Meta:
        model = User
        fields = [
            'email', 'password',
            'first_name', 'last_name',
            'phone_number',
            'birth_date',
            'gender',
            'timezone', 'language',
            'is_active',
            'is_email_verified',
            'is_push_enabled',
            'role_ids',
        ]

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Bu email band")
        return value

    def create(self, validated_data):
        role_ids = validated_data.pop('role_ids', [])
        password = validated_data.pop('password')

        user = User.objects.create_user(password=password, **validated_data)

        if role_ids:
            user.roles.set(role_ids)

        return user


class UserAdminUpdateSerializer(serializers.ModelSerializer):
    """Admin PATCH — barcha maydonlarni tahrirlay olish (parolsiz).

    Parol yangilash uchun alohida endpoint (`/admin/users/<id>/set-password/`)
    ishlatiladi — bu maxfiy operatsiyani ajratib qo'yish uchun.
    """
    role_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True,
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name',
            'phone_number',
            'birth_date',
            'gender',
            'timezone', 'language',
            'is_active',
            'is_email_verified',
            'is_push_enabled',
            'role_ids',
        ]

    def update(self, instance, validated_data):
        role_ids = validated_data.pop('role_ids', None)
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save()
        if role_ids is not None:
            instance.roles.set(role_ids)
        return instance


class UserAdminPasswordSerializer(serializers.Serializer):
    """Admin parol o'zgartirish — alohida endpoint."""
    password = serializers.CharField(min_length=6)
