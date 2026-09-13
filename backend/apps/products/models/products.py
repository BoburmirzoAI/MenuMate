from django.db import models

from apps.shared.models import BaseModel


class ShoppingList(BaseModel):
    """
    Menyudan hisoblab chiqarilgan xarid ro'yxati.
    """
    menu = models.OneToOneField(
        'menu.Menu', on_delete=models.CASCADE, related_name='shopping_list'
    )
    total_estimated_cost = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, help_text="Taxminiy jami narx (so'm)"
    )

    class Meta:
        db_table = 'products_shopping_list'

    def __str__(self):
        return f"Xarid ro'yxati: {self.menu}"


class ShoppingItem(BaseModel):
    shopping_list = models.ForeignKey(
        ShoppingList, on_delete=models.CASCADE, related_name='items'
    )
    ingredient = models.ForeignKey(
        'recipes.Ingredient', on_delete=models.PROTECT, related_name='shopping_items'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=10)
    is_purchased = models.BooleanField(default=False)

    class Meta:
        db_table = 'products_shopping_item'
        unique_together = ('shopping_list', 'ingredient')

    def __str__(self):
        return f"{self.ingredient.name_uz}: {self.total_amount}{self.unit}"
