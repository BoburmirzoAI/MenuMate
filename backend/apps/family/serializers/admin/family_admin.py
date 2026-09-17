"""Admin: Oilalar."""
from rest_framework import serializers

from apps.family.models.family import FamilyMember, FamilyProfile, HealthCondition


class _HealthConditionMini(serializers.ModelSerializer):
    class Meta:
        model = HealthCondition
        fields = ['id', 'name', 'category']


class _FamilyMemberMini(serializers.ModelSerializer):
    health_conditions = _HealthConditionMini(many=True, read_only=True)

    class Meta:
        model = FamilyMember
        fields = [
            'id', 'name', 'age', 'gender', 'avatar_emoji', 'health_conditions',
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
