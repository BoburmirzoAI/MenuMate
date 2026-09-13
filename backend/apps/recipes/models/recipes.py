"""
Recipes app modellari.
Tillar (uz/ru/en) `django-modeltranslation` orqali boshqariladi
(`apps/recipes/translation.py`ga qarang).
"""
from django.db import models

from apps.shared.models import BaseModel


class AllergenTag(BaseModel):
    """dukkakli, sut, tuxum, yong'oq, gluten va h.k."""
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        db_table = 'recipes_allergen_tag'
        ordering = ['slug']

    def __str__(self):
        return self.name


class Ingredient(BaseModel):
    class Category(models.TextChoices):
        VEGETABLE = 'VEGETABLE', 'Sabzavot'
        FRUIT = 'FRUIT', 'Meva'
        MEAT = 'MEAT', 'Go\'sht'
        DAIRY = 'DAIRY', 'Sut mahsuloti'
        GRAIN = 'GRAIN', 'Don mahsuloti'
        SPICE = 'SPICE', 'Ziravor'
        OIL = 'OIL', 'Yog\''
        OTHER = 'OTHER', 'Boshqa'

    class Unit(models.TextChoices):
        GRAM = 'g', 'gramm'
        KILOGRAM = 'kg', 'kilogramm'
        LITER = 'l', 'litr'
        MILLILITER = 'ml', 'millilitr'
        PIECE = 'pcs', 'dona'
        TSP = 'tsp', 'choy qoshiq'
        TBSP = 'tbsp', 'osh qoshiq'

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=Category.choices)
    default_unit = models.CharField(max_length=10, choices=Unit.choices, default=Unit.GRAM)
    image_url = models.URLField(blank=True, help_text="Ingredient rasmi")
    allergen_tags = models.ManyToManyField(AllergenTag, blank=True, related_name='ingredients')

    class Meta:
        db_table = 'recipes_ingredient'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class Recipe(BaseModel):
    class Category(models.TextChoices):
        BREAKFAST = 'BREAKFAST', 'Nonushta'
        LUNCH = 'LUNCH', 'Tushlik'
        DINNER = 'DINNER', 'Kechki ovqat'
        SALAD = 'SALAD', 'Salat'
        SOUP = 'SOUP', 'Sho\'rva'
        DRINK = 'DRINK', 'Ichimlik'
        DESSERT = 'DESSERT', 'Shirinlik'
        BREAD = 'BREAD', 'Non mahsuloti'
        SNACK = 'SNACK', 'Yengil taom'

    class Season(models.TextChoices):
        SUMMER = 'SUMMER', 'Yoz'
        WINTER = 'WINTER', 'Qish'
        AUTUMN = 'AUTUMN', 'Kuz'
        SPRING = 'SPRING', 'Bahor'
        ALL = 'ALL', 'Har doim'

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    category = models.CharField(max_length=20, choices=Category.choices)
    season = models.CharField(max_length=10, choices=Season.choices, default=Season.ALL)

    prep_time_minutes = models.PositiveIntegerField(help_text="Tayyorlash vaqti (daqiqa)")
    calories_per_serving = models.PositiveIntegerField(help_text="1 kishi uchun kaloriya")
    servings = models.PositiveIntegerField(default=1, help_text="Retsept nechchi kishi uchun")

    is_hot = models.BooleanField(default=True, help_text="Issiq ovqatmi (weather filter uchun)")
    image = models.ForeignKey(
        'shared.Media', on_delete=models.SET_NULL, null=True, blank=True, related_name='+'
    )
    image_url = models.URLField(blank=True, help_text="Retsept rasmi (Unsplash yoki CDN URL)")

    allergen_tags = models.ManyToManyField(AllergenTag, blank=True, related_name='recipes')

    class Meta:
        db_table = 'recipes_recipe'
        ordering = ['category', 'name']

    def __str__(self):
        return self.name


class RecipeIngredient(BaseModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT, related_name='used_in')
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="1 kishi uchun miqdor"
    )
    unit = models.CharField(max_length=10, choices=Ingredient.Unit.choices)

    class Meta:
        db_table = 'recipes_recipe_ingredient'
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f"{self.recipe.name}: {self.ingredient.name} {self.amount}{self.unit}"


class RecipeStep(BaseModel):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveSmallIntegerField()
    description = models.TextField()

    class Meta:
        db_table = 'recipes_recipe_step'
        ordering = ['order']
        unique_together = ('recipe', 'order')

    def __str__(self):
        return f"{self.recipe.name} — {self.order}-qadam"
