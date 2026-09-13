"""
Recipes tarjimalari — django-modeltranslation.

Har register qilingan field uchun DB'da `<field>_uz`, `<field>_ru`,
`<field>_en` ustunlar avtomatik yaratiladi.
"""
from modeltranslation.translator import TranslationOptions, register

from apps.recipes.models.recipes import (
    AllergenTag,
    Ingredient,
    Recipe,
    RecipeStep,
)


@register(AllergenTag)
class AllergenTagTranslation(TranslationOptions):
    fields = ('name',)


@register(Ingredient)
class IngredientTranslation(TranslationOptions):
    fields = ('name',)


@register(Recipe)
class RecipeTranslation(TranslationOptions):
    fields = ('name', 'description')


@register(RecipeStep)
class RecipeStepTranslation(TranslationOptions):
    fields = ('description',)
