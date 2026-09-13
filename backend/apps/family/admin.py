from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.family.models.family import (
    FamilyMember,
    FamilyProfile,
    HealthCondition,
)


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 0
    fields = ('name', 'age', 'gender')
    show_change_link = True


@admin.register(FamilyProfile)
class FamilyProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'family_name', 'user', 'city', 'members_count', 'created_at')
    list_filter = ('city',)
    search_fields = ('family_name', 'user__email', 'city')
    list_select_related = ('user',)
    inlines = [FamilyMemberInline]

    def members_count(self, obj):
        return obj.members.count()
    members_count.short_description = "A'zolar"


@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'family', 'age', 'gender', 'created_at')
    list_filter = ('gender',)
    search_fields = ('name', 'family__family_name', 'family__user__email')
    list_select_related = ('family', 'family__user')
    filter_horizontal = (
        'liked_recipes', 'disliked_recipes',
        'health_conditions', 'allergen_ingredients',
    )


@admin.register(HealthCondition)
class HealthConditionAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)
