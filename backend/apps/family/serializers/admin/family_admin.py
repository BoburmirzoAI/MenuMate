"""Admin: Oilalar."""
from rest_framework import serializers

from apps.family.models.family import FamilyMember, FamilyProfile, HealthCondition
from apps.users.models.users import User


class _HealthConditionMini(serializers.ModelSerializer):
    class Meta:
        model = HealthCondition
        fields = ['id', 'name', 'category']


class _FamilyMemberMini(serializers.ModelSerializer):
    health_conditions = _HealthConditionMini(many=True, read_only=True)

    class Meta:
        model = FamilyMember
        fields = [
            'id', 'name', 'age', 'gender', 'health_conditions',
        ]


class FamilyAdminListSerializer(serializers.ModelSerializer):
    """Grid uchun asosiy maydonlar + a'zolar soni."""
    member_count = serializers.SerializerMethodField()
    owner_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = FamilyProfile
        fields = ['id', 'family_name', 'city', 'member_count', 'owner_email', 'created_at']

    def get_member_count(self, obj) -> int:
        return obj.members.count() if hasattr(obj, 'members') else 0


class FamilyAdminDetailSerializer(FamilyAdminListSerializer):
    members = _FamilyMemberMini(many=True, read_only=True)

    class Meta(FamilyAdminListSerializer.Meta):
        fields = FamilyAdminListSerializer.Meta.fields + ['members']


class FamilyAdminCreateSerializer(serializers.ModelSerializer):
    """Admin yangi oila yaratadi — user ID bilan bog'lash kerak.

    Bitta foydalanuvchining bitta oilasi bo'lishi mumkin (OneToOne).
    """
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = FamilyProfile
        fields = ['user_id', 'family_name', 'city']

    def validate_user_id(self, value: int) -> int:
        if not User.objects.filter(id=value, is_deleted=False).exists():
            raise serializers.ValidationError("Foydalanuvchi topilmadi")
        if FamilyProfile.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("Bu foydalanuvchining oilasi bor")
        return value

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        return FamilyProfile.objects.create(user_id=user_id, **validated_data)


class FamilyAdminUpdateSerializer(serializers.ModelSerializer):
    """PATCH — nom va shahar."""

    class Meta:
        model = FamilyProfile
        fields = ['family_name', 'city']


# ═══════════════════════════════════════════════════════════════════════════
#  Family Members — batafsil CRUD
# ═══════════════════════════════════════════════════════════════════════════


class FamilyMemberAdminSerializer(serializers.ModelSerializer):
    """A'zoning to'liq ma'lumotlari + sog'liq holatlari va allergen ingredientlar."""
    health_conditions = _HealthConditionMini(many=True, read_only=True)
    health_condition_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=HealthCondition.objects.all(),
        write_only=True,
        required=False,
        source='health_conditions',
    )
    allergen_ingredient_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = FamilyMember
        fields = [
            'id',
            'family',
            'name', 'age', 'gender',
            'health_conditions',
            'health_condition_ids',
            'allergen_ingredient_ids',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        allergens = validated_data.pop('allergen_ingredient_ids', None)
        member = super().create(validated_data)
        if allergens is not None:
            member.allergen_ingredients.set(allergens)
        return member

    def update(self, instance, validated_data):
        allergens = validated_data.pop('allergen_ingredient_ids', None)
        member = super().update(instance, validated_data)
        if allergens is not None:
            member.allergen_ingredients.set(allergens)
        return member
