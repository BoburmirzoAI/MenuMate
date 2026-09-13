from django.contrib import admin

from apps.products.models.products import ShoppingItem, ShoppingList


class ShoppingItemInline(admin.TabularInline):
    model = ShoppingItem
    extra = 0
    autocomplete_fields = ('ingredient',)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'total_estimated_cost', 'created_at')
    search_fields = ('menu__family__family_name',)
    list_select_related = ('menu',)
    inlines = [ShoppingItemInline]


@admin.register(ShoppingItem)
class ShoppingItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopping_list', 'ingredient', 'total_amount', 'unit', 'is_purchased')
    list_filter = ('is_purchased', 'unit')
    search_fields = ('ingredient__name_uz',)
    list_select_related = ('shopping_list', 'ingredient')
