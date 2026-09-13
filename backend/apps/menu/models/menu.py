from django.db import models

from apps.shared.models import BaseModel


class Menu(BaseModel):
    class Duration(models.TextChoices):
        WEEKLY = 'WEEKLY', 'Haftalik'
        MONTHLY = 'MONTHLY', 'Oylik'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Faol'
        COMPLETED = 'COMPLETED', 'Tugallangan'

    family = models.ForeignKey(
        'family.FamilyProfile', on_delete=models.CASCADE, related_name='menus'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.CharField(
        max_length=10, choices=Duration.choices, default=Duration.WEEKLY
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE
    )
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'menu_menu'
        # Yangi menyu birinchi kelsin — start_date bir xil bo'lsa yaratilgani bilan aniq.
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f"{self.family.family_name}: {self.start_date} — {self.end_date}"


class MenuDay(BaseModel):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='days')
    date = models.DateField()
    is_holiday = models.BooleanField(default=False)
    holiday_name = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'menu_menu_day'
        ordering = ['date']
        unique_together = ('menu', 'date')

    def __str__(self):
        return f"{self.menu.family.family_name} — {self.date}"


class MenuMeal(BaseModel):
    """Nonushta / Tushlik / Kechki slot. Retseptlar `items` orqali biriktiriladi."""

    class MealType(models.TextChoices):
        BREAKFAST = 'BREAKFAST', 'Nonushta'
        LUNCH = 'LUNCH', 'Tushlik'
        DINNER = 'DINNER', 'Kechki'

    day = models.ForeignKey(MenuDay, on_delete=models.CASCADE, related_name='meals')
    meal_type = models.CharField(max_length=15, choices=MealType.choices)

    class Meta:
        db_table = 'menu_menu_meal'
        # BREAKFAST → LUNCH → DINNER tartibida (alfavit emas)
        ordering = ['id']
        unique_together = ('day', 'meal_type')

    def __str__(self):
        return f"{self.day.date} · {self.get_meal_type_display()}"


class MenuMealItem(BaseModel):
    """Bir slot ichidagi element: asosiy ovqat, salat, ichimlik va h.k."""

    class Category(models.TextChoices):
        MAIN = 'MAIN', 'Asosiy ovqat'
        SOUP = 'SOUP', "Sho'rva"
        SALAD = 'SALAD', 'Salat'
        DRINK = 'DRINK', 'Ichimlik'
        BREAD = 'BREAD', 'Non'
        DESSERT = 'DESSERT', 'Shirinlik'

    meal = models.ForeignKey(MenuMeal, on_delete=models.CASCADE, related_name='items')
    category = models.CharField(max_length=15, choices=Category.choices)
    recipe = models.ForeignKey(
        'recipes.Recipe', on_delete=models.PROTECT, related_name='menu_items'
    )

    class Meta:
        db_table = 'menu_menu_meal_item'
        ordering = ['category']
        unique_together = ('meal', 'category')

    def __str__(self):
        return f"{self.meal} · {self.get_category_display()}: {self.recipe.name}"
