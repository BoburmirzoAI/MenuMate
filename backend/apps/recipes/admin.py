from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.recipes.models.recipes import (
    AllergenTag,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeStep,
)


@admin.register(AllergenTag)
class AllergenTagAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'slug', 'name')
    search_fields = ('slug', 'name')


@admin.register(Ingredient)
class IngredientAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'name', 'category', 'default_unit')
    list_filter = ('category', 'default_unit')
    search_fields = ('name',)
    filter_horizontal = ('allergen_tags',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient',)


class RecipeStepInline(admin.StackedInline):
    """Nested inline uchun modeltranslation'da odatiy admin.StackedInline ishlatiladi."""
    model = RecipeStep
    extra = 1
    fields = ('order', 'description', 'description_ru', 'description_en')


@admin.register(Recipe)
class RecipeAdmin(TabbedTranslationAdmin):
    list_display = (
        'id', 'name', 'category', 'season',
        'prep_time_minutes', 'calories_per_serving', 'is_hot',
    )
    list_filter = ('category', 'season', 'is_hot')
    search_fields = ('name',)
    filter_horizontal = ('allergen_tags',)
    inlines = [RecipeIngredientInline, RecipeStepInline]


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount', 'unit')
    list_select_related = ('recipe', 'ingredient')
    search_fields = ('recipe__name', 'ingredient__name')


@admin.register(RecipeStep)
class RecipeStepAdmin(TabbedTranslationAdmin):
    list_display = ('id', 'recipe', 'order', 'description')
    list_select_related = ('recipe',)
    search_fields = ('recipe__name', 'description')
